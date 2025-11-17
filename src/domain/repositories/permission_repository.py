from abc import ABC, abstractmethod
from typing import Optional, List
from domain.models.permission import Permission


class PermissionRepository(ABC):

    @abstractmethod
    async def get_by_permission(self, permission: List[int]) -> Optional[Permission]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Permission]:
        pass

    @abstractmethod
    async def delete_permission(self, permission: str) -> bool:
        pass
