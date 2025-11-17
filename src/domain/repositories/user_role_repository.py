from abc import ABC, abstractmethod
from typing import Optional, List
from domain.models.user_role import UserRole, UserRoleBase


class UserRoleRepository(ABC):

    @abstractmethod
    async def get_by_user_id(self, current_user: dict) -> Optional[UserRole]:
        pass

    @abstractmethod
    async def get_all(self, current_user: dict) -> List[UserRole]:
        pass

    @abstractmethod
    async def update_user_role(self, id: int, user_role_update: UserRoleBase, current_user: dict) -> bool:
        pass
