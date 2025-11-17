from typing import List, Any

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from domain.models.user_role import UserRole, UserRoleBase
from domain.repositories.user_role_repository import UserRoleRepository
from infrastructure.orm.user_role_orm_model import UserRoleOrmModel
from fastapi import HTTPException
from datetime import datetime

from infrastructure.orm.orm_update_helper import update_orm_model_from_domain


class SQLUserRoleRepository(UserRoleRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all(self, current_user: dict) -> List[UserRole]:
        result = await self.db_session.execute(select(UserRoleOrmModel).filter(UserRoleOrmModel.is_deleted.is_(False)))
        orm_user_role = result.scalars().all()
        user_role = [item.to_domain() for item in orm_user_role]
        return user_role

    async def get_by_user_id(self, current_user: dict) -> Any:
        result = await self.db_session.execute(
            select(UserRoleOrmModel).filter(UserRoleOrmModel.user_id == current_user["user"].id,
                                            UserRoleOrmModel.is_deleted.is_(False)))
        orm_user_role = result.scalars().first()
        if orm_user_role is None:
            raise HTTPException(status_code=400, detail="Wrong User Role")

        user_role = orm_user_role.to_domain()
        return user_role

    async def update_user_role(self, id: int, update_user_role: UserRoleBase, current_user: dict) -> bool:
        result = await self.db_session.execute(
            select(UserRoleOrmModel).filter(UserRoleOrmModel.user_id == id, UserRoleOrmModel.is_deleted.is_(False)))
        orm_user_role = result.scalars().first()

        if orm_user_role is None:
            raise HTTPException(status_code=400, detail="Wrong User Role")

        orm_user_role = update_orm_model_from_domain(orm_user_role, update_user_role)
        orm_user_role.updated_at = datetime.now()
        orm_user_role.updated_by = current_user["user"].id

        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False