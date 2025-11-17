from typing import List, Any

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from domain.models.permission import Permission
from domain.repositories.permission_repository import PermissionRepository
from infrastructure.orm.permissions_orm_model import PermissionOrmModel
from fastapi import HTTPException
from datetime import datetime
from sqlalchemy import func
from db_error_handlers import handle_db_errors


class SQLPermissionRepository(PermissionRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    @handle_db_errors
    async def get_all(self) -> List[Permission]:
        result = await self.db_session.execute(select(PermissionOrmModel).filter(PermissionOrmModel.is_deleted.is_(False)))
        orm_permission = result.scalars().all()
        permissions = [item.to_domain() for item in orm_permission]
        return permissions

    @handle_db_errors
    async def get_by_permission(self, permission_ids: List[int]) -> Any:
        result = await self.db_session.execute(
            select(PermissionOrmModel).filter(PermissionOrmModel.id.in_(permission_ids), PermissionOrmModel.is_deleted.is_(False)))
        orm_permissions = result.scalars().all()

        if not orm_permissions or len(orm_permissions) != len(permission_ids):
            raise HTTPException(status_code=400, detail="Wrong Permission")

        permissions = [item.to_domain() for item in orm_permissions]
        return permissions

    @handle_db_errors
    async def delete_permission(self, current_user: dict, name: str) -> bool:
        result = await self.db_session.execute(
            select(PermissionOrmModel).filter(PermissionOrmModel.name == name, PermissionOrmModel.is_deleted.is_(False)))
        orm_permission = result.scalars().first()

        if orm_permission is None:
            raise HTTPException(status_code=400, detail="Wrong Permission")

        orm_permission.updated_at = datetime.now()
        orm_permission.is_deleted = True
        orm_permission.deleted_at = datetime.now()
        orm_permission.updated_by = current_user["user"].id
        orm_permission.deleted_by = current_user["user"].id
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False

    @handle_db_errors
    async def verify_permission_ids_exist(self, permission_ids: List[int]) -> bool:
        result = await self.db_session.execute(
            select(func.count(PermissionOrmModel.id)).filter(
                PermissionOrmModel.id.in_(permission_ids),
                PermissionOrmModel.is_deleted.is_(False)
            )
        )
        count = result.scalar()

        if count != len(permission_ids):
            raise HTTPException(status_code=400, detail="Wrong Permission")

        return True
