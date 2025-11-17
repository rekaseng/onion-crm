from typing import List

from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from domain.models.member_groups import MemberGroup, MemberGroupBase
from domain.repositories.member_groups_repository import MemberGroupsRepository
from infrastructure.orm.member_groups_orm_model import MemberGroupOrmModel
from fastapi import HTTPException
from datetime import datetime

from infrastructure.orm.orm_update_helper import update_orm_model_from_domain
import re


def generate_slug(name: str) -> str:
    # Convert to lowercase and replace spaces with hyphens
    slug = name.lower().replace(" ", "-")
    # Remove any characters that are not alphanumeric or hyphens
    slug = re.sub(r"[^a-z0-9-]", "", slug)
    return slug


class SQLMemberGroupsRepository(MemberGroupsRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all(self, tenant_id: int) -> List[MemberGroup]:
        result = await self.db_session.execute(
            select(MemberGroupOrmModel).filter(
                MemberGroupOrmModel.is_deleted.is_(False)),
                MemberGroupOrmModel.tenant_id == tenant_id
        )
        orm_member_groups = result.scalars().all()
        member_groups = [item.to_domain() for item in orm_member_groups]
        return member_groups

    async def get_all_admin(self, tenant_id: int) -> List[MemberGroup]:
        query = select(MemberGroupOrmModel).filter(MemberGroupOrmModel.tenant_id == tenant_id,
                                               MemberGroupOrmModel.is_deleted.is_(False))
        result = await self.db_session.execute(query)
        orm_member_groups = result.scalars().all()
        member_groups = [item.to_domain() for item in orm_member_groups]
        return member_groups

    async def add(self, member_groups: MemberGroup) -> bool:
        result = await self.db_session.execute(
            select(MemberGroupOrmModel).filter(MemberGroupOrmModel.slug == member_groups.slug,
                                               MemberGroupOrmModel.is_deleted.is_(False)))
        orm_member_groups = result.scalars().first()

        if orm_member_groups:
            raise HTTPException(status_code=400, detail="MemberGroups with this code already exists")

        slug = generate_slug(member_groups.name)
        member_groups.slug = slug
        orm_member_groups = MemberGroupOrmModel.from_domain(member_groups)
        await self.db_session.merge(orm_member_groups)
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False

    async def get_one(self, id: int):
        result = await self.db_session.execute(
            select(MemberGroupOrmModel).filter(MemberGroupOrmModel.id == id)
        )
        orm_member_group = result.scalars().first()
        if orm_member_group is None:
            raise HTTPException(status_code=400, detail="Wrong MemberGroup")

        member_group = orm_member_group.to_domain()
        return member_group

    async def get_by_slug(self, slug: str, current_user: dict) -> MemberGroup:
        result = await self.db_session.execute(
            select(MemberGroupOrmModel).filter(MemberGroupOrmModel.slug == slug,
                                               MemberGroupOrmModel.is_deleted.is_(False)))
        orm_member_group = result.scalars().first()

        if orm_member_group is None:
            raise HTTPException(status_code=400, detail="Wrong MemberGroup")

        member_group = orm_member_group.to_domain()
        return member_group

    async def get_by_slug_admin(self, slug: str, current_user: dict) -> MemberGroup:
        result = await self.db_session.execute(
            select(MemberGroupOrmModel).filter(MemberGroupOrmModel.tenant_id == current_user["tenant"].id,
                                               MemberGroupOrmModel.slug == slug,
                                               MemberGroupOrmModel.is_deleted.is_(False)))
        orm_member_groups = result.scalars().first()

        if orm_member_groups is None:
            raise HTTPException(status_code=400, detail="Wrong MemberGroups")

        member_groups = orm_member_groups.to_domain()
        return member_groups

    async def update_member_group(self, update_member_groups: MemberGroup, current_user: dict) -> bool:
        member_groups_result = await self.db_session.execute(
            select(MemberGroupOrmModel).filter(MemberGroupOrmModel.id == update_member_groups.id,
                                               MemberGroupOrmModel.is_deleted.is_(False)))
        orm_member_groups = member_groups_result.scalars().first()

        if orm_member_groups is None:
            raise HTTPException(status_code=400, detail="Wrong MemberGroups")
        orm_member_groups = update_orm_model_from_domain(orm_member_groups, update_member_groups)
        orm_member_groups.name = update_member_groups.name
        orm_member_groups.slug = generate_slug(update_member_groups.name)
        orm_member_groups.updated_at = datetime.now()
        orm_member_groups.created_by = current_user["user"].id
        orm_member_groups.updated_by = current_user["user"].id
        orm_member_groups.deleted_by = None
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False

    async def update_member_group_admin(self, tenant_id: int, current_user_id: int, id: int, update_member_group: MemberGroupBase) -> bool:
        member_groups_result = await self.db_session.execute(
            select(MemberGroupOrmModel).filter(MemberGroupOrmModel.tenant_id == tenant_id,
                                               MemberGroupOrmModel.id == id,
                                               MemberGroupOrmModel.is_deleted.is_(False)))
        orm_member_groups = member_groups_result.scalars().first()

        if orm_member_groups is None:
            raise HTTPException(status_code=400, detail="Wrong MemberGroups")
        orm_member_groups = update_orm_model_from_domain(orm_member_groups, update_member_group)
        orm_member_groups.name = update_member_group.name
        orm_member_groups.slug = generate_slug(update_member_group.name)
        orm_member_groups.updated_at = datetime.now()
        orm_member_groups.updated_by = current_user_id
        orm_member_groups.deleted_by = None
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False

    async def delete_member_groups(self, slug: str, current_user: dict) -> bool:
        member_groups_result = await self.db_session.execute(
            select(MemberGroupOrmModel).filter(MemberGroupOrmModel.slug == slug,
                                               MemberGroupOrmModel.is_deleted.is_(False)))
        orm_member_groups = member_groups_result.scalars().first()

        if orm_member_groups is None:
            raise HTTPException(status_code=400, detail="Wrong MemberGroups")

        orm_member_groups.updated_at = datetime.now()
        orm_member_groups.is_deleted = True
        orm_member_groups.deleted_at = datetime.now()
        orm_member_groups.created_by = current_user["user"].id
        orm_member_groups.updated_by = current_user["user"].id
        orm_member_groups.deleted_by = current_user["user"].id
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False

    async def delete_member_groups_admin(self, tenant_id: int, user_id:int, id: int) -> bool:
        result = await self.db_session.execute(
            select(MemberGroupOrmModel).filter(MemberGroupOrmModel.tenant_id == tenant_id,
                                               MemberGroupOrmModel.id == id,
                                               MemberGroupOrmModel.is_deleted.is_(False)))
        orm_member_group = result.scalars().first()

        if orm_member_group is None:
            raise HTTPException(status_code=400, detail="Wrong MemberGroups")

        orm_member_group.updated_at = datetime.now()
        orm_member_group.is_deleted = True
        orm_member_group.deleted_at = datetime.now()
        orm_member_group.deleted_by = user_id
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False
    
    async def get_by_user_id(self, user_id: int) -> List[MemberGroup]:
        result = await self.db_session.execute(
            select(MemberGroupOrmModel).filter(or_(MemberGroupOrmModel.user_ids.contains([user_id]), MemberGroupOrmModel.all_users.is_(True)),
                                               MemberGroupOrmModel.is_deleted.is_(False)))
        orm_member_groups = result.scalars().all()

        if orm_member_groups is None:
            raise HTTPException(status_code=400, detail="Wrong MemberGroups")

        return [item.to_domain() for item in orm_member_groups]