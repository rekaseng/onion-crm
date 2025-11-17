from typing import List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from domain.models.tenant import Tenant, TenantBase
from domain.repositories.tenant_repository import TenantRepository
from infrastructure.orm.tenant_orm_model import TenantOrmModel
from fastapi import HTTPException
from datetime import datetime

from infrastructure.orm.orm_update_helper import update_orm_model_from_domain


class SQLTenantRepository(TenantRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all(self, current_user: dict) -> List[Tenant]:
        result = await self.db_session.execute(
            select(TenantOrmModel).filter(TenantOrmModel.is_deleted.is_(False))
        )
        orm_tenant = result.scalars().all()
        tenants = [item.to_domain() for item in orm_tenant]
        return tenants

    async def add(self, tenant: Tenant, current_user: dict) -> bool:
        tenant_result = await self.db_session.execute(select(TenantOrmModel).filter_by(name=tenant.name))
        orm_tenant = tenant_result.scalars().first()

        if orm_tenant:
            raise HTTPException(status_code=400, detail="Tenant with this code already exists")

        orm_tenant = TenantOrmModel.from_domain(tenant)
        await self.db_session.merge(orm_tenant)
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False

    async def get_by_tenant(self, name: str, current_user: dict) -> Tenant:
        result = await self.db_session.execute(
            select(TenantOrmModel).filter(TenantOrmModel.name == name, TenantOrmModel.is_deleted.is_(False)))
        orm_tenant = result.scalars().first()

        if orm_tenant is None:
            raise HTTPException(status_code=400, detail="Wrong Tenant")

        tenant = orm_tenant.to_domain()
        return tenant

    async def get_by_id(self, tenant_id: int, current_user: dict) -> Tenant:
        result = await self.db_session.execute(
            select(TenantOrmModel).filter(TenantOrmModel.id == tenant_id, TenantOrmModel.is_deleted.is_(False)))
        orm_tenant = result.scalars().first()

        if orm_tenant is None:
            raise HTTPException(status_code=400, detail="Wrong Tenant")

        tenant = orm_tenant.to_domain()
        return tenant

    async def update_tenant(self, id:int, update_tenant: TenantBase, current_user: dict) -> bool:
        result = await self.db_session.execute(
            select(TenantOrmModel).filter(TenantOrmModel.id == id,
                                          TenantOrmModel.is_deleted.is_(False)))
        orm_tenant = result.scalars().first()

        if orm_tenant is None:
            raise HTTPException(status_code=400, detail="Wrong Tenant")

        orm_tenant = update_orm_model_from_domain(orm_tenant, update_tenant)
        orm_tenant.updated_at = datetime.now()
        orm_tenant.updated_by = current_user["user"].id

        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False

    async def delete_tenant(self, id: int, current_user: dict) -> bool:
        result = await self.db_session.execute(
            select(TenantOrmModel).filter(TenantOrmModel.id == id, TenantOrmModel.is_deleted.is_(False)))
        orm_tenant = result.scalars().first()

        if orm_tenant is None:
            raise HTTPException(status_code=400, detail="Wrong Tenant")

        orm_tenant.updated_at = datetime.now()
        orm_tenant.is_deleted = True
        orm_tenant.deleted_at = datetime.now()
        orm_tenant.deleted_by = current_user["user"].id
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False