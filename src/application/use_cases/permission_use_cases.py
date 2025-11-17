from typing import List

from domain.models.permission import Permission
from domain.repositories.permission_repository import PermissionRepository


class PermissionUseCases:
    def __init__(self, permission_repository: PermissionRepository):
        self.permission_repository = permission_repository

    async def get_all(self) -> List[Permission]:
        permissions = await self.permission_repository.get_all()
        return permissions

    async def get_by_permission(self, permission: List[int]) -> Permission:
        permission = await self.permission_repository.get_by_permission(permission)
        return permission

    async def delete_permission(self, permission: str) -> bool:
        permission = await self.permission_repository.delete_permission(permission)
        return permission
