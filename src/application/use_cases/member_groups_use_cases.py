from typing import List

from domain.models.member_groups import MemberGroup, MemberGroupBase
from domain.repositories.member_groups_repository import MemberGroupsRepository
from datetime import datetime


class MemberGroupUseCases:
    def __init__(self, member_groups_repository: MemberGroupsRepository):
        self.member_groups_repository = member_groups_repository

    async def add(self, member_groups_dto: MemberGroupBase, user_id: int, tenant_id: int) -> bool:
        member_groups = MemberGroup(
            created_at=datetime.now(),
            updated_at=datetime.now(),
            is_active=True,
            name=member_groups_dto.name,
            slug=member_groups_dto.name,
            tenant_id=tenant_id,
            is_global=False,
            is_deleted=False,
            deleted_at=None,
            created_by=user_id,
            updated_by=user_id,
            deleted_by=None
        )
        await self.member_groups_repository.add(member_groups)
        return member_groups

    async def get_all(self, current_user: dict) -> List[MemberGroup]:
        member_groups = await self.member_groups_repository.get_all(current_user)
        return member_groups

    async def get_all_admin(self, current_user: dict) -> List[MemberGroup]:
        member_groups = await self.member_groups_repository.get_all_admin(current_user)
        return member_groups

    async def get_one(self, id: int) -> MemberGroup:
        member_groups = await self.member_groups_repository.get_one(id)
        return member_groups

    async def get_by_slug(self, slug: str, current_user: dict) -> MemberGroup:
        member_groups = await self.member_groups_repository.get_by_slug(slug, current_user)
        return member_groups

    async def get_by_slug_admin(self, slug: str, current_user: dict) -> MemberGroup:
        member_groups = await self.member_groups_repository.get_by_slug_admin(slug, current_user)
        return member_groups

    async def update_member_group(self, member_groups_update_dto: MemberGroupBase, current_user: dict) -> bool:
        member_group = await self.member_groups_repository.update_member_group(member_groups_update_dto, current_user)
        return member_group

    async def update_member_group_admin(self, tenant_id: int, user_id: int, id: int, member_group_update_dto: MemberGroupBase) -> bool:
        member_group = await self.member_groups_repository.update_member_group_admin(tenant_id, user_id, id,
                                                                                     member_group_update_dto)
        return member_group

    async def delete_member_groups(self, slug: str, current_user: dict) -> bool:
        member_group = await self.member_groups_repository.delete_member_groups(slug, current_user)
        return member_group

    async def delete_member_groups_admin(self, tenant_id, user_id: int, id: int) -> bool:
        member_group = await self.member_groups_repository.delete_member_groups_admin(tenant_id, user_id, id)
        return member_group
