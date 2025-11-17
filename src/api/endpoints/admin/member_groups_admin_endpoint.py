from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from application.dto.auth_dto import UserAuthDTO
from domain.models.member_groups import MemberGroupBase
from api.deps import get_db, get_current_user, check_permission, get_admin, get_current_user_auth
from application.use_cases.member_groups_use_cases import MemberGroupUseCases
from infrastructure.repositories.sql_member_groups_repository import SQLMemberGroupsRepository
from fastapi import HTTPException
from typing import List

router = APIRouter()


@router.post("/", response_model=dict)
async def member_groups_admin_add(
        member_groups_dto: MemberGroupBase,
        current_user_auth: UserAuthDTO = Depends(get_current_user_auth),
        permission: bool = Depends(check_permission("member_groups_write")),
        is_admin: bool = Depends(get_admin),
        db: AsyncSession = Depends(get_db)
):
    member_groups_repository = SQLMemberGroupsRepository(db)
    member_groups_service = MemberGroupUseCases(member_groups_repository)
    new_member_groups = await member_groups_service.add(member_groups_dto, current_user_auth.user.id, current_user_auth.tenant.id)
    if new_member_groups is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong Member Group")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": [new_member_groups]
    }


@router.get("/", response_model=dict)
async def get_admin_member_groups(
        current_user_auth: UserAuthDTO = Depends(get_current_user_auth),
        permission: bool = Depends(check_permission("member_groups_read")),
        is_admin: bool = Depends(get_admin),
        db: AsyncSession = Depends(get_db)
):
    member_group_repository = SQLMemberGroupsRepository(db)
    member_group_service = MemberGroupUseCases(member_group_repository)
    tenant_id = current_user_auth.tenant.id
    member_group = await member_group_service.get_all_admin(tenant_id)
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": {"items":member_group}
    }


@router.get("/{id}", response_model=dict)
async def get_admin_member_group(
        id: int,
        current_user_auth: UserAuthDTO = Depends(get_current_user_auth),
        permission: bool = Depends(check_permission("member_groups_read")),
        is_admin: bool = Depends(get_admin),
        db: AsyncSession = Depends(get_db)
):
    member_group_repository = SQLMemberGroupsRepository(db)
    member_group_service = MemberGroupUseCases(member_group_repository)
    member_group = await member_group_service.get_one(id)
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": member_group
    }


@router.put("/{id}", response_model=dict)
async def member_groups_admin_update(
        id: int,
        member_groups_update_dto: MemberGroupBase,
        current_user_auth: UserAuthDTO = Depends(get_current_user_auth),
        permission: bool = Depends(check_permission("member_groups_write")),
        is_admin: bool = Depends(get_admin),
        db: AsyncSession = Depends(get_db)
):
    member_groups_repository = SQLMemberGroupsRepository(db)
    member_groups_service = MemberGroupUseCases(member_groups_repository)
    user_id = current_user_auth.user.id
    tenant_id = current_user_auth.tenant.id
    member_group = await member_groups_service.update_member_group_admin(tenant_id, user_id, id, member_groups_update_dto)
    if member_group is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Member Group Update Unsuccessful")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": []
    }


@router.delete("/{id}", response_model=dict)
async def remove_member_groups_admin(
        id: int,
        current_user_auth: UserAuthDTO = Depends(get_current_user_auth),
        permission: bool = Depends(check_permission("member_groups_write")),
        is_admin: bool = Depends(get_admin),
        db: AsyncSession = Depends(get_db)
):
    member_groups_repository = SQLMemberGroupsRepository(db)
    member_groups_service = MemberGroupUseCases(member_groups_repository)
    user_id = current_user_auth.user.id
    tenant_id= current_user_auth.tenant.id
    member_group = await member_groups_service.delete_member_groups_admin(tenant_id, user_id, id)
    if member_group is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Member Group Delete Unsuccessful")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": []
    }
