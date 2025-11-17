from typing import List

from domain.models.tenant import Tenant, TenantBase
from domain.repositories.tenant_repository import TenantRepository
from datetime import datetime


class TenantUseCases:
    def __init__(self, tenant_repository: TenantRepository):
        self.tenant_repository = tenant_repository

    async def add(self, tenant_dto: TenantBase, current_user: dict) -> bool:
        tenant = Tenant(
            created_at=datetime.now(),
            updated_at=datetime.now(),
            name=tenant_dto.name,
            main_contact_name=tenant_dto.main_contact_name,
            main_contact_mobile=tenant_dto.main_contact_mobile,
            main_contact_email=tenant_dto.main_contact_email,
            main_contact_address=tenant_dto.main_contact_address,
            admin=tenant_dto.admin,
            is_deleted=False,
            deleted_at=None,
            created_by=current_user["user"].id,
            updated_by=current_user["user"].id,
            deleted_by=None
        )
        await self.tenant_repository.add(tenant, current_user)
        return tenant

    async def get_all(self, current_user: dict) -> List[Tenant]:
        tenants = await self.tenant_repository.get_all(current_user)
        return tenants

    async def get_by_tenant(self, name: str, current_user: dict) -> Tenant:
        tenant = await self.tenant_repository.get_by_tenant(name, current_user)
        return tenant

    async def get_by_id(self, tenant_id: int, current_user: dict) -> Tenant:
        tenant = await self.tenant_repository.get_by_id(tenant_id, current_user)
        return tenant

    async def update_tenant(self, id:int, update_tenant_dto: TenantBase, current_user: dict) -> bool:
        tenant = await self.tenant_repository.update_tenant(id, update_tenant_dto, current_user)
        return tenant

    async def delete_tenant(self, id: int, current_user: dict) -> bool:
        tenant = await self.tenant_repository.delete_tenant(id, current_user)
        return tenant
