from abc import ABC, abstractmethod
from typing import Optional, List
from domain.models.role import Role, RoleBase


class RoleRepository(ABC):

    @abstractmethod
    async def add(self, role: Role, current_user: dict) -> bool:
        pass

    @abstractmethod
    async def add_admin(self, role: Role, current_user: dict) -> bool:
        pass

    @abstractmethod
    async def get_by_id(self, id: int, current_user: dict) -> Optional[Role]:
        pass

    @abstractmethod
    async def get_by_role_admin(self, role: str, current_user: dict) -> Optional[Role]:
        pass

    @abstractmethod
    async def get_by_id(self, role_id: int, current_user: dict) -> Optional[Role]:
        pass

    @abstractmethod
    async def get_all(self, current_user: dict) -> List[Role]:
        pass

    @abstractmethod
    async def get_all_admin(self, current_user: dict) -> List[Role]:
        pass

    @abstractmethod
    async def update_role(self, id:int, update_role: RoleBase, current_user: dict) -> bool:
        pass

    @abstractmethod
    async def update_role_admin(self, id:int, update_role: RoleBase, current_user: dict) -> bool:
        pass

    @abstractmethod
    async def delete_role(self, id: int, current_user: dict) -> bool:
        pass

    @abstractmethod
    async def delete_role_admin(self, id: int, current_user: dict) -> bool:
        pass
