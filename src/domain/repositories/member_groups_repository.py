from abc import ABC, abstractmethod
from typing import Optional, List
from domain.models.member_groups import MemberGroup, MemberGroupBase


class MemberGroupsRepository(ABC):
    @abstractmethod
    async def add(self, member_groups: MemberGroup) -> bool:
        pass

    @abstractmethod
    async def get_by_slug(self, slug: str, current_user: dict) -> Optional[MemberGroup]:
        pass

    @abstractmethod
    async def get_by_slug_admin(self, slug: str, current_user: dict) -> Optional[MemberGroup]:
        pass

    @abstractmethod
    async def get_all(self, tenant_id: int) -> List[MemberGroup]:
        pass
    @abstractmethod
    async def get_one(self, id: int):
        pass

    @abstractmethod
    async def get_all_admin(self, tenant_id: int) -> List[MemberGroup]:
        pass

    @abstractmethod
    async def update_member_group(self, member_groups_update_dto: MemberGroupBase, current_user: dict) -> bool:
        pass

    @abstractmethod
    async def update_member_group_admin(self, tenant_id: int, current_user_id: int, id: int, update_member_group: MemberGroupBase) -> bool:
        pass

    @abstractmethod
    async def delete_member_groups(self, slug: str, current_user: dict) -> bool:
        pass

    @abstractmethod
    async def delete_member_groups_admin(self, tenant_id: int, user_id: int, int: id) -> bool:
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> List[MemberGroup]:
        pass
