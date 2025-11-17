from typing import List

from domain.models.member_group_users import MemberGroupUsers, MemberGroupUsersBase
from domain.repositories.member_group_users_repository import MemberGroupUsersRepository
from datetime import datetime


class MemberGroupUsersUseCases:
    def __init__(self, member_group_users_repository: MemberGroupUsersRepository):
        self.member_group_users_repository = member_group_users_repository

    async def add(self, member_group_users_dto: MemberGroupUsersBase, current_user: dict) -> bool:
        member_group_users = MemberGroupUsers(
            created_at=datetime.now(),
            updated_at=datetime.now(),
            member_group_id=member_group_users_dto.member_group_id,
            user_id=member_group_users_dto.user_id,
            is_deleted=False,
            deleted_at=None,
            created_by=current_user["user"].id,
            updated_by=current_user["user"].id,
            deleted_by=None
        )
        await self.member_group_users_repository.add(member_group_users, current_user)
        return member_group_users

    async def add_admin(self, member_group_users_dto: MemberGroupUsersBase, current_user: dict) -> bool:
        member_group_users = MemberGroupUsers(
            created_at=datetime.now(),
            updated_at=datetime.now(),
            member_group_id=member_group_users_dto.member_group_id,
            user_id=member_group_users_dto.user_id,
            is_deleted=False,
            deleted_at=None,
            created_by=current_user["user"].id,
            updated_by=current_user["user"].id,
            deleted_by=None
        )
        await self.member_group_users_repository.add_admin(member_group_users, current_user)
        return member_group_users

    async def get_all(self, current_user: dict) -> List[MemberGroupUsers]:
        member_group_users = await self.member_group_users_repository.get_all(current_user)
        return member_group_users

    async def get_all_admin(self, current_user: dict) -> List[MemberGroupUsers]:
        member_group_users = await self.member_group_users_repository.get_all_admin(current_user)
        return member_group_users

    async def get_by_user_id(self, user_id: int, current_user: dict) -> MemberGroupUsers:
        member_group_users = await self.member_group_users_repository.get_by_user_id(user_id, current_user)
        return member_group_users

    async def get_by_user_id_admin(self, user_id: int, current_user: dict) -> MemberGroupUsers:
        member_group_users = await self.member_group_users_repository.get_by_user_id_admin(user_id, current_user)
        return member_group_users

    async def update_member_group_users(self, member_group_users_update_dto: MemberGroupUsersBase, current_user: dict) -> bool:
        member_group_user = await self.member_group_users_repository.update_member_group_users(
            member_group_users_update_dto, current_user)
        return member_group_user

    async def update_member_group_users_admin(self, member_group_users_update_dto: MemberGroupUsersBase,
                                              current_user: dict) -> bool:
        member_group_user = await self.member_group_users_repository.update_member_group_users_admin(
            member_group_users_update_dto,
            current_user)
        return member_group_user

    async def delete_member_group_users(self, user_id: int, current_user: dict) -> bool:
        member_group_user = await self.member_group_users_repository.delete_member_group_users(user_id, current_user)
        return member_group_user

    async def delete_member_group_users_admin(self, user_id: int, current_user: dict) -> bool:
        member_group_user = await self.member_group_users_repository.delete_member_group_users_admin(user_id,
                                                                                                     current_user)
        return member_group_user
