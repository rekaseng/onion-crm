from abc import ABC, abstractmethod
from typing import Optional, List
from domain.models.member_group_users import MemberGroupUsers, MemberGroupUsersBase


class MemberGroupUsersRepository(ABC):
    @abstractmethod
    async def add(self, member_group_users: MemberGroupUsers, current_user: dict) -> bool:
        pass

    @abstractmethod
    async def add_admin(self, member_group_users: MemberGroupUsers, current_user: dict) -> bool:
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: int, current_user: dict) -> Optional[MemberGroupUsers]:
        pass

    @abstractmethod
    async def get_by_user_id_admin(self, user_id: int, current_user: dict) -> Optional[MemberGroupUsers]:
        pass

    @abstractmethod
    async def get_all(self, current_user: dict) -> List[MemberGroupUsers]:
        pass

    @abstractmethod
    async def get_all_admin(self, current_user: dict) -> List[MemberGroupUsers]:
        pass

    @abstractmethod
    async def update_member_group_users(self, member_group_users_update_dto: MemberGroupUsersBase, current_user: dict) -> bool:
        pass

    @abstractmethod
    async def update_member_group_users_admin(self, member_group_users_update_dto: MemberGroupUsersBase, current_user: dict) -> bool:
        pass

    @abstractmethod
    async def delete_member_group_users(self, user_id: int, current_user: dict) -> bool:
        pass

    @abstractmethod
    async def delete_member_group_users_admin(self, user_id: int, current_user: dict) -> bool:
        pass
