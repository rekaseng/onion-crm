from typing import List, Union

from fastapi.logger import logger
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from domain.models.user import User, UpdatePassword, UserBase
from domain.repositories.user_repository import UserRepository
from infrastructure.orm.user_orm_model import UserOrmModel
from infrastructure.orm.user_role_orm_model import UserRoleOrmModel
from infrastructure.orm.tenant_orm_model import TenantOrmModel
from infrastructure.orm.role_orm_model import RoleOrmModel
from infrastructure.orm.user_qr_keys_orm_model import UserQrKeysOrmModel
from infrastructure.orm.payment_method_orm_model import PaymentMethodOrmModel
from infrastructure.orm.store_credits_orm_model import StoreCreditsOrmModel
from fastapi import HTTPException
from datetime import datetime
from infrastructure.orm.reward_point_orm_model import RewardPointOrmModel
from utils.security import create_qr_payload

from infrastructure.orm.orm_update_helper import update_orm_model_from_domain
from domain.models.user_message import UserMessage
from infrastructure.orm.user_message_orm_model import UserMessageOrmModel


class SQLUserRepository(UserRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all(self, current_user: dict) -> List[User]:
        result = await self.db_session.execute(select(UserOrmModel))
        orm_users = result.scalars().all()
        users = [item.to_domain() for item in orm_users]
        return users

    async def add_user(self, user: User) -> bool:
        user_result = await self.db_session.execute(select(UserOrmModel).filter_by(email=user.email))
        orm_user = user_result.scalars().first()

        if orm_user:
            raise HTTPException(status_code=400, detail="Wrong User")

        orm_user = UserOrmModel.from_domain(user)
        self.db_session.add(orm_user)

        await self.db_session.flush()  # Ensure the orm_user.id is generated before using it

        orm_user_role = UserRoleOrmModel(
            created_at=datetime.now(),
            updated_at=datetime.now(),
            user_id=orm_user.id,
            role_id=1,  # role_id 1 for admin
            is_deleted=False,
            deleted_at=None,
            created_by=orm_user.id,
            updated_by=orm_user.id,
            deleted_by=None
        )
        self.db_session.add(orm_user_role)
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError as e:
            print(e)
            await self.db_session.rollback()
            # Log the error details
            logger.error("Failed to commit user addition", exc_info=True)
            return False

    async def add_user_admin(self, tenant_id: int, user_admin: User, current_user: dict) -> bool:
        tenant_result = await self.db_session.execute(select(TenantOrmModel).filter_by(id=tenant_id))
        orm_tenant = tenant_result.scalars().first()

        if not orm_tenant:
            raise HTTPException(status_code=400, detail="Wrong Tenant")

        role_name = orm_tenant.name + "-admin"
        role_result = await self.db_session.execute(select(RoleOrmModel).filter_by(name=role_name))
        orm_role = role_result.scalars().first()

        if orm_role:
            raise HTTPException(status_code=400, detail="Role exists")

        orm_role = RoleOrmModel(
            created_at=datetime.now(),
            updated_at=datetime.now(),
            name=orm_tenant.name+"-admin",
            permissions=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
            tenant_id=orm_tenant.id,
            is_deleted=False,
            deleted_at=None,
            created_by=1,
            updated_by=1,
            deleted_by=None,
            is_admin=True,
            is_hq_admin=False
        )
        self.db_session.add(orm_role)

        await self.db_session.flush()  # Ensure the orm_role.id is generated before using it

        user_result = await self.db_session.execute(select(UserOrmModel).filter_by(mobile=user_admin.mobile))
        orm_user = user_result.scalars().first()

        if orm_user:
            raise HTTPException(status_code=400, detail="Wrong User")

        orm_user = UserOrmModel.from_domain(user_admin)
        orm_user.tenant_id = orm_tenant.id
        self.db_session.add(orm_user)

        await self.db_session.flush()  # Ensure the orm_user.id is generated before using it

        orm_user_role = UserRoleOrmModel(
            created_at=datetime.now(),
            updated_at=datetime.now(),
            user_id=orm_user.id,
            role_id=orm_role.id,
            is_deleted=False,
            deleted_at=None,
            created_by=orm_user.id,
            updated_by=orm_user.id,
            deleted_by=None
        )
        self.db_session.add(orm_user_role)
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False

    async def register(self, user: User) -> None:
        user_result = await self.db_session.execute(select(UserOrmModel).filter_by(mobile=user.mobile))
        orm_user = user_result.scalars().first()

        if orm_user:
            raise HTTPException(status_code=400, detail="Wrong User")
        
        role_result = await self.db_session.execute(select(RoleOrmModel).filter_by(name='normal-user', is_deleted=False))
        orm_role = role_result.scalars().first()

        if not orm_role:
            raise HTTPException(status_code=400, detail="Normal User role was not found")

        orm_user = UserOrmModel.from_domain(user)
        self.db_session.add(orm_user)

        await self.db_session.flush()  # Ensure the orm_user.id is generated before using it

        orm_user_role = UserRoleOrmModel(
            created_at=datetime.now(),
            updated_at=datetime.now(),
            user_id=orm_user.id,
            role_id=orm_role.id,  # role_id 1 for admin
            is_deleted=False,
            deleted_at=None,
            created_by=orm_user.id,
            updated_by=orm_user.id,
            deleted_by=None
        )
        self.db_session.add(orm_user_role)
        initial_balance = 0.00
        store_credit = StoreCreditsOrmModel(
            user_id=orm_user.id,
            balance=initial_balance,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            is_deleted=False,
            created_by=orm_user.id,
            updated_by=orm_user.id,
            deleted_by=None
        )
        self.db_session.add(store_credit)

        reward_point = RewardPointOrmModel(
            user_id=orm_user.id,
            balance=initial_balance,
            points=0,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            is_deleted=False,
            created_by=orm_user.id,
            updated_by=orm_user.id,
            deleted_by=None
        )
        self.db_session.add(reward_point)

        # Commit the changes to the database
        await self.db_session.commit()


    async def get_by_full_mobile(self, full_mobile: str):
        result = await self.db_session.execute(
            select(UserOrmModel).filter(UserOrmModel.full_mobile == full_mobile))
        orm_user = result.scalars().first()
        if orm_user:
            user = orm_user.to_domain()
            return user
        else:
            return None

    async def get_by_id(self, user_id: int) -> Union[User, None]:
        result = await self.db_session.execute(
            select(UserOrmModel).filter(UserOrmModel.id == user_id, UserOrmModel.is_deleted.is_(False)))
        orm_user = result.scalars().first()

        if orm_user is None:
            raise HTTPException(status_code=400, detail="Wrong User")

        result = await self.db_session.execute(
            select(StoreCreditsOrmModel).filter(
                StoreCreditsOrmModel.user_id == user_id,
                StoreCreditsOrmModel.is_deleted.is_(False)
            ))
        store_credit = result.scalars().first()

        user = orm_user.to_domain()

        if store_credit:
            user.credits = store_credit.balance
        else:
            user.credits = 0
        return user

    async def update_password(self, update_password: UpdatePassword, current_user: dict) -> bool:
        result = await self.db_session.execute(
            select(UserOrmModel).filter(UserOrmModel.email == update_password.email,
                                        UserOrmModel.is_deleted.is_(False)))
        orm_user = result.scalars().first()

        if orm_user is None:
            raise HTTPException(status_code=400, detail="Wrong User")

        credential_result = await self.db_session.execute(
            select(UserOrmModel).filter_by(email=update_password.email,
                                           password=update_password.current_password))
        orm_user = credential_result.scalars().first()

        if orm_user is None:
            # Check if the password is correct
            raise HTTPException(status_code=400, detail="Wrong username/password")

        if update_password.current_password == update_password.new_password:
            raise HTTPException(
                status_code=400, detail="New password cannot be the same as the current one"
            )

        # Update the user's password
        orm_user.password = update_password.new_password
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False

    async def update_user_info(self, id: int, update_user_info: UserBase,) -> bool:
        result = await self.db_session.execute(
            select(UserOrmModel).filter(UserOrmModel.id == id,
                                        UserOrmModel.is_deleted.is_(False)))
        orm_user = result.scalars().first()
        if orm_user is None:
            raise HTTPException(status_code=400, detail="Wrong User")

        orm_user = update_orm_model_from_domain(orm_user, update_user_info)
        orm_user.updated_at = datetime.now()
        orm_user.updated_by = id

        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False

    async def delete_user(self, user_id: int, current_user: dict) -> bool:
        result = await self.db_session.execute(
            select(UserOrmModel).filter(UserOrmModel.id == user_id, UserOrmModel.is_deleted.is_(False)))
        orm_user = result.scalars().first()

        if orm_user is None:
            raise HTTPException(status_code=400, detail="Wrong User")

        orm_user.updated_at = datetime.now()
        orm_user.is_deleted = True
        orm_user.deleted_at = datetime.now()
        orm_user.updated_by = current_user["user"].id
        orm_user.deleted_by = current_user["user"].id

        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False

    async def get_profile(self, current_user: dict) -> Union[User, None]:
        result = await self.db_session.execute(
            select(UserOrmModel).filter(UserOrmModel.id == current_user["user"].id, UserOrmModel.is_deleted.is_(False)))
        orm_user = result.scalars().first()

        if orm_user is None:
            raise HTTPException(status_code=400, detail="Wrong User")

        user = orm_user.to_domain()

        return user

    async def get_user_qr_key(self, key_name) -> UserQrKeysOrmModel:
        result = await self.db_session.execute(
            select(UserQrKeysOrmModel).filter(UserQrKeysOrmModel.name == key_name))
        orm_user_qr_key = result.scalars().first()
        if orm_user_qr_key is None:
            raise HTTPException(status_code=400, detail="Wrong User Qr Keys")

        return orm_user_qr_key
    async def get_active_key_name(self) -> str:
        result = await self.db_session.execute(
            select(UserQrKeysOrmModel).filter(UserQrKeysOrmModel.is_active == True))
        orm_user_key_name = result.scalars().first()
        if orm_user_key_name is None:
            raise HTTPException(status_code=400, detail="Wrong User Qr Keys")

        return orm_user_key_name.name

    async def get_qr_code(self, current_user: dict, key_name: str) -> str:
        result = await self.db_session.execute(
            select(UserQrKeysOrmModel).filter(UserOrmModel.id == current_user["user"].id,
                                              UserOrmModel.is_deleted.is_(False)))
        orm_user = result.scalars().first()

        if orm_user is None:
            raise HTTPException(status_code=400, detail="Wrong User")
        user_id = current_user["user"].id

        result = await self.db_session.execute(
            select(PaymentMethodOrmModel)
            .filter(
                PaymentMethodOrmModel.user_id == user_id,
                PaymentMethodOrmModel.card_type != "",
                PaymentMethodOrmModel.is_deleted.is_(False)
            )
        )

        payment_method = result.scalars().first()
        if payment_method:
            linked_credit_card=1
        else:
            linked_credit_card=0

        result = await self.db_session.execute(
            select(StoreCreditsOrmModel).filter(
                StoreCreditsOrmModel.user_id == user_id,
                StoreCreditsOrmModel.is_deleted.is_(False)
            ))
        store_credit = result.scalars().first()

        if store_credit:
            store_credit_in_cents = int(store_credit.balance * 100)
            if store_credit_in_cents < 0:
                store_credit_str = f"n{abs(store_credit_in_cents)}"
            else:
                store_credit_str = f"{store_credit_in_cents}"
        else:
            store_credit_str = "0"

        qr_payload = create_qr_payload(user_id, store_credit_str, linked_credit_card, key_name)
        return qr_payload

    async def save_message(self, user_message: UserMessage) -> None:
        orm_message = UserMessageOrmModel.from_domain(user_message)
        self.db_session.add(orm_message)
        await self.db_session.commit()

    async def get_user_messages(self, user_id: int) -> List[UserMessage]:
        result = await self.db_session.execute(
            select(UserMessageOrmModel)
            .filter(UserMessageOrmModel.user_id == user_id)
            .order_by(UserMessageOrmModel.created_at.desc())
        )
        orm_messages = result.scalars().all()
        return [message.to_domain() for message in orm_messages]