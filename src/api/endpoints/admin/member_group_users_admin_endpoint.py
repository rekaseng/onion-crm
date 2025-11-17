from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from domain.models.member_group_users import MemberGroupUsersBase
from api.deps import get_db, get_current_user, check_permission, get_admin
from application.use_cases.member_group_users_use_cases import MemberGroupUsersUseCases
from infrastructure.repositories.sql_member_group_users_repository import SQLMemberGroupUsersRepository
from fastapi import HTTPException
from typing import List

router = APIRouter()


@router.post("/", response_model=dict)
async def member_group_users_add_admin(
        member_group_users_dto: MemberGroupUsersBase,
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("member_groups_write")),
        is_admin: bool = Depends(get_admin),
        db: AsyncSession = Depends(get_db)
):
    member_group_users_repository = SQLMemberGroupUsersRepository(db)
    member_group_users_service = MemberGroupUsersUseCases(member_group_users_repository)
    new_member_group_users = await member_group_users_service.add_admin(member_group_users_dto, current_user)
    if new_member_group_users is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong Member Group User")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": new_member_group_users
    }


@router.get("/", response_model=dict)
async def get_member_group_users_admin(
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("member_groups_read")),
        is_admin: bool = Depends(get_admin),
        db: AsyncSession = Depends(get_db)
):
    member_group_users_repository = SQLMemberGroupUsersRepository(db)
    member_group_users_service = MemberGroupUsersUseCases(member_group_users_repository)
    member_group_users = await member_group_users_service.get_all_admin(current_user)
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": {"items": member_group_users}
    }


@router.get("/{user_id}", response_model=dict)
async def get_member_group_user_admin(
        user_id: int,
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("member_groups_read")),
        is_admin: bool = Depends(get_admin),
        db: AsyncSession = Depends(get_db)
):
    member_group_users_repository = SQLMemberGroupUsersRepository(db)
    member_group_users_service = MemberGroupUsersUseCases(member_group_users_repository)
    member_group_users = await member_group_users_service.get_by_user_id_admin(user_id, current_user)
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": member_group_users
    }


@router.put("/{user_id}", response_model=dict)
async def member_group_users_update_admin(
        member_group_users_update_dto: MemberGroupUsersBase,
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("member_groups_write")),
        is_admin: bool = Depends(get_admin),
        db: AsyncSession = Depends(get_db)
):
    member_group_users_repository = SQLMemberGroupUsersRepository(db)
    member_group_users_service = MemberGroupUsersUseCases(member_group_users_repository)
    member_group_user = await member_group_users_service.update_member_group_users_admin(member_group_users_update_dto, current_user)
    if member_group_user is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Member Group User Update Unsuccessful")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": []
    }


@router.delete("/{user_id}", response_model=dict)
async def remove_member_group_users_admin(
        user_id: int,
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("member_groups_write")),
        is_admin: bool = Depends(get_admin),
        db: AsyncSession = Depends(get_db)
):
    member_group_users_repository = SQLMemberGroupUsersRepository(db)
    member_group_users_service = MemberGroupUsersUseCases(member_group_users_repository)
    member_group_user = await member_group_users_service.delete_member_group_users_admin(user_id, current_user)
    if member_group_user is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Member Group User Update Unsuccessful")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": []
    }