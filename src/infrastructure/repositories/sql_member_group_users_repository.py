from typing import List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from domain.models.member_group_users import MemberGroupUsers, MemberGroupUsersBase
from domain.repositories.member_group_users_repository import MemberGroupUsersRepository
from infrastructure.orm.member_group_users_orm_model import MemberGroupUsersOrmModel
from infrastructure.orm.user_orm_model import UserOrmModel
from infrastructure.orm.member_groups_orm_model import MemberGroupOrmModel

from fastapi import HTTPException
from datetime import datetime

from infrastructure.orm.orm_update_helper import update_orm_model_from_domain


class SQLMemberGroupUsersRepository(MemberGroupUsersRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all(self, current_user: dict) -> List[MemberGroupUsers]:
        result = await self.db_session.execute(
            select(MemberGroupUsersOrmModel).filter(MemberGroupUsersOrmModel.is_deleted.is_(False)))
        orm_member_group_users = result.scalars().all()
        member_group_users = [item.to_domain() for item in orm_member_group_users]
        return member_group_users

    async def get_all_admin(self, current_user: dict) -> List[MemberGroupUsers]:
        result = await self.db_session.execute(
            select(MemberGroupUsersOrmModel)
            .join(MemberGroupOrmModel, MemberGroupUsersOrmModel.member_group_id == MemberGroupOrmModel.id)
            .filter(MemberGroupOrmModel.tenant_id == current_user["tenant"].id,
                    MemberGroupUsersOrmModel.is_deleted.is_(False))
        )
        orm_member_group_users = result.scalars().all()
        member_group_users = [item.to_domain() for item in orm_member_group_users]
        return member_group_users

    async def add(self, member_group_users: MemberGroupUsers, current_user: dict) -> bool:
        user_result = await self.db_session.execute(select(UserOrmModel).filter_by(id=member_group_users.user_id))
        orm_user = user_result.scalars().first()

        if not orm_user:
            raise HTTPException(status_code=400, detail="Wrong User")

        member_groups_result = await self.db_session.execute(
            select(MemberGroupOrmModel).filter_by(id=member_group_users.member_group_id))
        orm_member_groups = member_groups_result.scalars().first()

        if not orm_member_groups:
            raise HTTPException(status_code=400, detail="Wrong MemberGroup")

        result = await self.db_session.execute(
            select(MemberGroupUsersOrmModel).filter(MemberGroupUsersOrmModel.user_id == member_group_users.user_id,
                                                    MemberGroupUsersOrmModel.is_deleted.is_(False)))
        orm_member_group_users = result.scalars().first()

        if orm_member_group_users:
            raise HTTPException(status_code=400, detail="MemberGroupUser already exists")

        orm_member_group_users = MemberGroupUsersOrmModel.from_domain(member_group_users)
        await self.db_session.merge(orm_member_group_users)
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False

    async def add_admin(self, member_group_users: MemberGroupUsers, current_user: dict) -> bool:
        user_result = await self.db_session.execute(select(UserOrmModel).filter_by(id=member_group_users.user_id))
        orm_user = user_result.scalars().first()

        if not orm_user:
            raise HTTPException(status_code=400, detail="Wrong User")

        member_groups_result = await self.db_session.execute(
            select(MemberGroupOrmModel).filter(MemberGroupOrmModel.tenant_id == current_user["tenant"].id,
                                               MemberGroupOrmModel.id == member_group_users.member_group_id,
                                               MemberGroupOrmModel.is_deleted.is_(False)))
        orm_member_groups = member_groups_result.scalars().first()

        if not orm_member_groups:
            raise HTTPException(status_code=400, detail="Wrong MemberGroup")

        result = await self.db_session.execute(
            select(MemberGroupUsersOrmModel)
            .join(MemberGroupOrmModel, MemberGroupUsersOrmModel.member_group_id == MemberGroupOrmModel.id)
            .filter(MemberGroupUsersOrmModel.user_id == member_group_users.user_id,
                    MemberGroupOrmModel.tenant_id == current_user["tenant"].id,
                    MemberGroupUsersOrmModel.is_deleted.is_(False))
        )
        orm_member_group_users = result.scalars().first()

        if orm_member_group_users:
            raise HTTPException(status_code=400, detail="MemberGroupUser already exists")

        orm_member_group_users = MemberGroupUsersOrmModel.from_domain(member_group_users)
        await self.db_session.merge(orm_member_group_users)
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False

    async def get_by_user_id(self, user_id: int, current_user: dict) -> MemberGroupUsers:
        user_result = await self.db_session.execute(select(UserOrmModel).filter_by(id=user_id))
        orm_user = user_result.scalars().first()

        if not orm_user:
            raise HTTPException(status_code=400, detail="Wrong User")

        result = await self.db_session.execute(
            select(MemberGroupUsersOrmModel).filter(MemberGroupUsersOrmModel.user_id == user_id,
                                                    MemberGroupUsersOrmModel.is_deleted.is_(False)))
        orm_member_group_users = result.scalars().first()

        if orm_member_group_users is None:
            raise HTTPException(status_code=400, detail="Wrong MemberGroupUser")

        member_group_users = orm_member_group_users.to_domain()
        return member_group_users

    async def get_by_user_id_admin(self, user_id: int, current_user: dict) -> MemberGroupUsers:
        user_result = await self.db_session.execute(select(UserOrmModel).filter_by(id=user_id))
        orm_user = user_result.scalars().first()

        if not orm_user:
            raise HTTPException(status_code=400, detail="Wrong User")

        result = await self.db_session.execute(
            select(MemberGroupUsersOrmModel)
            .join(MemberGroupOrmModel, MemberGroupUsersOrmModel.member_group_id == MemberGroupOrmModel.id)
            .filter(MemberGroupOrmModel.tenant_id == current_user["tenant"].id,
                    MemberGroupUsersOrmModel.user_id == user_id,
                    MemberGroupUsersOrmModel.is_deleted.is_(False))
        )

        orm_member_group_users = result.scalars().first()

        if orm_member_group_users is None:
            raise HTTPException(status_code=400, detail="Wrong MemberGroupUser")

        member_group_users = orm_member_group_users.to_domain()
        return member_group_users

    async def update_member_group_users(self, update_member_group_users: MemberGroupUsers, current_user: dict) -> bool:
        user_result = await self.db_session.execute(
            select(UserOrmModel).filter_by(id=update_member_group_users.user_id))
        orm_user = user_result.scalars().first()

        if not orm_user:
            raise HTTPException(status_code=400, detail="Wrong User")

        member_groups_result = await self.db_session.execute(
            select(MemberGroupOrmModel).filter_by(id=update_member_group_users.member_group_id))
        orm_member_groups = member_groups_result.scalars().first()

        if not orm_member_groups:
            raise HTTPException(status_code=400, detail="Wrong MemberGroup")

        member_group_users_result = await self.db_session.execute(
            select(MemberGroupUsersOrmModel).filter(
                MemberGroupUsersOrmModel.user_id == update_member_group_users.user_id,
                MemberGroupUsersOrmModel.is_deleted.is_(False)))
        orm_member_group_users = member_group_users_result.scalars().first()

        if orm_member_group_users is None:
            raise HTTPException(status_code=400, detail="Wrong MemberGroupUser")

        orm_member_group_users = update_orm_model_from_domain(orm_member_group_users, update_member_group_users)
        orm_member_group_users.updated_at = datetime.now()
        orm_member_group_users.created_by = current_user["user"].id
        orm_member_group_users.updated_by = current_user["user"].id
        orm_member_group_users.deleted_by = None
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False

    async def update_member_group_users_admin(self, update_member_group_users: MemberGroupUsers, current_user: dict) -> bool:
        user_result = await self.db_session.execute(
            select(UserOrmModel).filter_by(id=update_member_group_users.user_id))
        orm_user = user_result.scalars().first()

        if not orm_user:
            raise HTTPException(status_code=400, detail="Wrong User")

        member_group_result = await self.db_session.execute(
            select(MemberGroupUsersOrmModel).filter(
                MemberGroupOrmModel.id == update_member_group_users.member_group_id,
                MemberGroupOrmModel.tenant_id == current_user["tenant"].id,
                MemberGroupUsersOrmModel.is_deleted.is_(False)))
        orm_member_group = member_group_result.scalars().first()

        if not orm_member_group:
            raise HTTPException(status_code=400, detail="Wrong MemberGroup")

        result = await self.db_session.execute(
            select(MemberGroupUsersOrmModel)
            .join(MemberGroupOrmModel, MemberGroupUsersOrmModel.member_group_id == MemberGroupOrmModel.id)
            .filter(MemberGroupOrmModel.tenant_id == current_user["tenant"].id,
                    MemberGroupUsersOrmModel.user_id == update_member_group_users.user_id,
                    MemberGroupUsersOrmModel.is_deleted.is_(False))
        )
        orm_member_group_users = result.scalars().first()

        if orm_member_group_users is None:
            raise HTTPException(status_code=400, detail="Wrong MemberGroupUser")

        orm_member_group_users = update_orm_model_from_domain(orm_member_group_users, update_member_group_users)
        orm_member_group_users.updated_at = datetime.now()
        orm_member_group_users.created_by = current_user["user"].id
        orm_member_group_users.updated_by = current_user["user"].id
        orm_member_group_users.deleted_by = None
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False

    async def delete_member_group_users(self, user_id: int, current_user: dict) -> bool:
        member_group_users_result = await self.db_session.execute(
            select(MemberGroupUsersOrmModel).filter(MemberGroupUsersOrmModel.user_id == user_id,
                                                    MemberGroupUsersOrmModel.is_deleted.is_(False)))
        orm_member_group_users = member_group_users_result.scalars().first()

        if orm_member_group_users is None:
            raise HTTPException(status_code=400, detail="Wrong MemberGroupUser")

        orm_member_group_users.updated_at = datetime.now()
        orm_member_group_users.is_deleted = True
        orm_member_group_users.deleted_at = datetime.now()
        orm_member_group_users.created_by = current_user["user"].id
        orm_member_group_users.updated_by = current_user["user"].id
        orm_member_group_users.deleted_by = current_user["user"].id
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False

    async def delete_member_group_users_admin(self, user_id: int, current_user: dict) -> bool:
        result = await self.db_session.execute(
            select(MemberGroupUsersOrmModel)
            .join(MemberGroupOrmModel, MemberGroupUsersOrmModel.member_group_id == MemberGroupOrmModel.id)
            .filter(MemberGroupOrmModel.tenant_id == current_user["tenant"].id,
                    MemberGroupUsersOrmModel.user_id == user_id,
                    MemberGroupUsersOrmModel.is_deleted.is_(False))
        )
        orm_member_group_users = result.scalars().first()

        if orm_member_group_users is None:
            raise HTTPException(status_code=400, detail="Wrong MemberGroupUser")

        orm_member_group_users.updated_at = datetime.now()
        orm_member_group_users.is_deleted = True
        orm_member_group_users.deleted_at = datetime.now()
        orm_member_group_users.created_by = current_user["user"].id
        orm_member_group_users.updated_by = current_user["user"].id
        orm_member_group_users.deleted_by = current_user["user"].id
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False