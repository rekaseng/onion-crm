import datetime
from utils import security

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from domain.models.login import Login, Token, Message
from domain.repositories.auth_repository import AuthRepository
from infrastructure.orm.user_orm_model import UserOrmModel
from infrastructure.orm.user_role_orm_model import UserRoleOrmModel
from fastapi import HTTPException
from utils.security import get_password_hash, create_access_token, verify_password


class SQLAuthRepository(AuthRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def login_access_token(self, form_data: Login) -> Token:
        full_mobile = f"{form_data.country_code}{form_data.mobile}"
        result = await self.db_session.execute(select(UserOrmModel).filter(UserOrmModel.full_mobile == full_mobile))
        orm_user = result.scalars().first()
        if orm_user is None:
            raise HTTPException(status_code=400, detail="Wrong User")
        if not verify_password(form_data.password, orm_user.password):
            raise HTTPException(status_code=400, detail="Wrong Username / Password")

        user = orm_user.to_domain()

        user_role_result = await self.db_session.execute(select(UserRoleOrmModel).filter(UserRoleOrmModel.user_id == user.id))
        orm_user_role = user_role_result.scalars().first()

        user_role = orm_user_role.to_domain()

        if not user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        access_token_expires = datetime.timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
        return Token(
            access_token=create_access_token(user.id, user_role.role_id, user.tenant_id, expires_delta=access_token_expires)
        )

    async def reset_password(self, full_mobile: str, new_password: str) -> Message:
        user_result = await self.db_session.execute(select(UserOrmModel).filter(UserOrmModel.full_mobile==full_mobile))
        orm_user = user_result.scalars().first()
        if not orm_user:
            raise HTTPException(
                status_code=400,
                detail="Wrong User",
            )

        if not orm_user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")

        hashed_password = get_password_hash(password=new_password)
        print("hashed_password"+hashed_password)
        orm_user.password = hashed_password
        await self.db_session.commit()
        return Message(message="Password updated successfully")


