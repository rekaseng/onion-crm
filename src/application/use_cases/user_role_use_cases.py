from typing import List

from domain.models.user_role import UserRole, UserRoleBase
from domain.repositories.user_role_repository import UserRoleRepository


class UserRoleUseCases:
    def __init__(self, user_role_repository: UserRoleRepository):
        self.user_role_repository = user_role_repository

    async def get_all(self, current_user: dict) -> List[UserRole]:
        user_roles = await self.user_role_repository.get_all(current_user)
        return user_roles

    async def get_by_user_id(self, current_user: dict) -> UserRole:
        user_role = await self.user_role_repository.get_by_user_id(current_user)
        return user_role

    async def update_user_role(self, id: int, user_role_update: UserRoleBase, current_user: dict) -> bool:
        user_role = await self.user_role_repository.update_user_role(id, user_role_update, current_user)
        return user_role
