from abc import ABC, abstractmethod
from typing import Optional, List
from domain.models.tenant import Tenant, TenantBase


class TenantRepository(ABC):

    @abstractmethod
    async def add(self, tenant: Tenant, current_user: dict) -> bool:
        pass

    @abstractmethod
    async def get_by_tenant(self, tenant: str, current_user: dict) -> Optional[Tenant]:
        pass

    @abstractmethod
    async def get_by_id(self, tenant_id: str, current_user: dict) -> Optional[Tenant]:
        pass

    @abstractmethod
    async def get_all(self, current_user: dict) -> List[Tenant]:
        pass

    @abstractmethod
    async def update_tenant(self, id: int, update_tenant: TenantBase, current_user: dict) -> bool:
        pass

    @abstractmethod
    async def delete_tenant(self, tenant: str, current_user: dict) -> bool:
        pass
