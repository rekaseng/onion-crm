from typing import List
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from domain.models.role import Role, RoleBase
from domain.repositories.role_repository import RoleRepository
from infrastructure.orm.role_orm_model import RoleOrmModel
from infrastructure.orm.tenant_orm_model import TenantOrmModel
from fastapi import HTTPException
from datetime import datetime
from infrastructure.orm.orm_update_helper import update_orm_model_from_domain

class SQLRoleRepository(RoleRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all(self, current_user: dict) -> List[Role]:
        result = await self.db_session.execute(select(RoleOrmModel).filter(RoleOrmModel.is_deleted.is_(False)))
        orm_role = result.scalars().all()
        roles = [item.to_domain() for item in orm_role]
        return roles

    async def get_all_admin(self, current_user: dict) -> List[Role]:
        result = await self.db_session.execute(
            select(RoleOrmModel).filter(RoleOrmModel.tenant_id == current_user["tenant"].id,
                                        RoleOrmModel.is_deleted.is_(False)))
        orm_role = result.scalars().all()
        roles = [item.to_domain() for item in orm_role]
        return roles

    async def add(self, role: Role, current_user: dict) -> bool:
        tenant_result = await self.db_session.execute(select(TenantOrmModel).filter_by(id=role.tenant_id))
        orm_tenant = tenant_result.scalars().first()

        if not orm_tenant:
            raise HTTPException(status_code=400, detail="Wrong Tenant")

        role_result = await self.db_session.execute(select(RoleOrmModel).filter_by(name=role.name))
        orm_role = role_result.scalars().first()

        if orm_role:
            raise HTTPException(status_code=400, detail="Role with this code already exists")

        orm_role = RoleOrmModel.from_domain(role)
        await self.db_session.merge(orm_role)

        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False

    async def add_admin(self, role: Role, current_user: dict) -> bool:  # Added return type
        result = await self.db_session.execute(select(RoleOrmModel).filter(
            RoleOrmModel.name == role.name,
            RoleOrmModel.tenant_id == current_user["tenant"].id,
            RoleOrmModel.is_deleted.is_(False)
        ))
        orm_role = result.scalars().first()

        if orm_role:
            raise HTTPException(status_code=400, detail="This Role already exists")

        orm_role = RoleOrmModel.from_domain(role)
        await self.db_session.merge(orm_role)

        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False

    async def get_by_role(self, name: str, current_user: dict) -> Role:
        result = await self.db_session.execute(
            select(RoleOrmModel).filter(RoleOrmModel.name == name, RoleOrmModel.is_deleted.is_(False)))
        orm_role = result.scalars().first()

        if orm_role is None:
            raise HTTPException(status_code=400, detail="Wrong Role")

        return orm_role.to_domain()

    async def get_by_role_admin(self, name: str, current_user: dict) -> Role:
        result = await self.db_session.execute(
            select(RoleOrmModel).filter(
                RoleOrmModel.name == name,
                RoleOrmModel.tenant_id == current_user["tenant"].id,
                RoleOrmModel.is_deleted.is_(False)
            ))
        orm_role = result.scalars().first()

        if orm_role is None:
            raise HTTPException(status_code=400, detail="Wrong Role")

        role = orm_role.to_domain()
        return role

    async def get_by_id(self, role_id: int, current_user: dict) -> Role:
        result = await self.db_session.execute(
            select(RoleOrmModel).filter(RoleOrmModel.id == role_id, RoleOrmModel.is_deleted.is_(False))
        )
        orm_role = result.scalars().first()

        if orm_role is None:
            raise HTTPException(status_code=400, detail="Wrong Role")

        role = orm_role.to_domain()
        return role

    async def update_role(self, update_role: RoleBase, current_user: dict) -> bool:
        result = await self.db_session.execute(
            select(RoleOrmModel).filter(RoleOrmModel.id == update_role.id, RoleOrmModel.is_deleted.is_(False))
        )
        orm_role = result.scalars().first()

        if orm_role is None:
            raise HTTPException(status_code=400, detail="Wrong Role")

        orm_role = update_orm_model_from_domain(orm_role, update_role)
        orm_role.updated_at = datetime.now()
        orm_role.updated_by = current_user["user"].id

        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False

    async def update_role_admin(self, id: int, update_role: RoleBase, current_user: dict) -> bool:
        result = await self.db_session.execute(select(RoleOrmModel).filter(RoleOrmModel.id == id))
        orm_role = result.scalars().first()

        if orm_role is None:
            raise HTTPException(status_code=400, detail="Wrong Role")

        orm_role = update_orm_model_from_domain(orm_role, update_role)
        orm_role.updated_at = datetime.now()
        orm_role.updated_by = current_user["user"].id

        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False

    async def delete_role(self, id: int, current_user: dict) -> bool:
        result = await self.db_session.execute(
            select(RoleOrmModel).filter(RoleOrmModel.id == id, RoleOrmModel.is_deleted.is_(False))
        )
        orm_role = result.scalars().first()

        if orm_role is None:
            raise HTTPException(status_code=400, detail="Wrong Role")

        orm_role.updated_at = datetime.now()
        orm_role.is_deleted = True
        orm_role.deleted_at = datetime.now()
        orm_role.deleted_by = current_user["user"].id

        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False

    async def delete_role_admin(self, id: int, current_user: dict) -> bool:
        result = await self.db_session.execute(
            select(RoleOrmModel).filter(
                RoleOrmModel.id == id,
                RoleOrmModel.tenant_id == current_user["tenant"].id,
                RoleOrmModel.is_deleted.is_(False)
            ))
        orm_role = result.scalars().first()

        if orm_role is None:
            raise HTTPException(status_code=400, detail="Wrong Role")

        orm_role.updated_at = datetime.now()
        orm_role.is_deleted = True
        orm_role.deleted_at = datetime.now()
        orm_role.deleted_by = current_user["user"].id

        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False
