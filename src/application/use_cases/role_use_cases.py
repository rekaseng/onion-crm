from typing import List

from domain.models.role import Role, RoleBase
from domain.repositories.role_repository import RoleRepository
from datetime import datetime


class RoleUseCases:
    def __init__(self, role_repository: RoleRepository):
        self.role_repository = role_repository

    async def add(self, role_dto: RoleBase, current_user: dict) -> bool:
        role = Role(
            created_at=datetime.now(),
            updated_at=datetime.now(),
            name=current_user["tenant"].name+"-"+role_dto.name,
            permissions=role_dto.permissions,
            tenant_id=current_user["tenant"].id,
            is_admin=False,
            is_hq_admin=False,
            is_deleted=False,
            deleted_at=None,
            created_by=current_user["user"].id,
            updated_by=current_user["user"].id,
            deleted_by=None
        )
        await self.role_repository.add(role, current_user)
        return role

    async def add_admin(self, role_dto: RoleBase, current_user: dict) -> bool:
        role = Role(
            created_at=datetime.now(),
            updated_at=datetime.now(),
            name=role_dto.name,
            permissions=role_dto.permissions,
            tenant_id=current_user["tenant"].id,
            is_global=False,
            is_deleted=False,
            deleted_at=None,
            created_by=current_user["user"].id,
            updated_by=current_user["user"].id,
            deleted_by=None
        )
        await self.role_repository.add_admin(role, current_user)
        return role

    async def get_all(self, current_user: dict) -> List[Role]:
        roles = await self.role_repository.get_all(current_user)
        return roles

    async def get_all_admin(self, current_user: dict) -> List[Role]:
        roles = await self.role_repository.get_all_admin(current_user)
        return roles

    async def get_by_role(self, role: str, current_user: dict) -> Role:
        role = await self.role_repository.get_by_role(role, current_user)
        return role

    async def get_by_role_admin(self, role: str, current_user: dict) -> Role:
        role = await self.role_repository.get_by_role_admin(role, current_user)
        return role

    async def get_by_id(self, role_id: int, current_user: dict) -> Role:
        role = await self.role_repository.get_by_id(role_id, current_user)
        return role

    async def update_role(self, role_id: int, update_role_dto: RoleBase, current_user: dict) -> bool:
        role = await self.role_repository.update_role(role_id, update_role_dto, current_user)
        return role

    async def update_role_admin(self, role_id: int, update_role_dto: RoleBase, current_user: dict) -> bool:
        role = await self.role_repository.update_role_admin(role_id, update_role_dto, current_user)
        return role

    async def delete_role(self, role_id: int, current_user: dict) -> bool:
        role = await self.role_repository.delete_role(role_id, current_user)
        return role

    async def delete_role_admin(self, role_id: int, current_user: dict) -> bool:
        role = await self.role_repository.delete_role_admin(role_id, current_user)
        return role
