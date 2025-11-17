from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from domain.models.member_groups import MemberGroupBase
from api.deps import get_db, get_current_user, check_permission
from application.use_cases.member_groups_use_cases import MemberGroupUseCases
from infrastructure.repositories.sql_member_groups_repository import SQLMemberGroupsRepository
from fastapi import HTTPException
from typing import List

router = APIRouter()


@router.post("/", response_model=dict)
async def member_groups_add(
        member_groups_dto: MemberGroupBase,
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("member_groups_write")),
        db: AsyncSession = Depends(get_db)
):
    member_groups_repository = SQLMemberGroupsRepository(db)
    member_groups_service = MemberGroupUseCases(member_groups_repository)
    new_member_groups = await member_groups_service.add(member_groups_dto, current_user)
    if new_member_groups is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong Member Group")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": [new_member_groups.dict()]
    }


@router.get("/", response_model=dict)
async def get_member_groups(
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("member_groups_read")),
        db: AsyncSession = Depends(get_db)
):
    member_groups_repository = SQLMemberGroupsRepository(db)
    member_groups_service = MemberGroupUseCases(member_groups_repository)
    member_groups = await member_groups_service.get_all(current_user)
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": {"items": member_groups}
    }


@router.get("/{slug}", response_model=dict)
async def get_member_group(
        slug: str,
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("member_groups_read")),
        db: AsyncSession = Depends(get_db)
):
    member_groups_repository = SQLMemberGroupsRepository(db)
    member_groups_service = MemberGroupUseCases(member_groups_repository)
    member_groups = await member_groups_service.get_by_slug(slug, current_user)
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": member_groups
    }


@router.put("/{slug}", response_model=dict)
async def member_groups_update(
        member_groups_update_dto: MemberGroupBase,
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("member_groups_write")),
        db: AsyncSession = Depends(get_db)
):
    member_groups_repository = SQLMemberGroupsRepository(db)
    member_groups_service = MemberGroupUseCases(member_groups_repository)
    member_group = await member_groups_service.update_member_group(member_groups_update_dto, current_user)
    if member_group is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Member Group Update Unsuccessful")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": []
    }


@router.delete("/{slug}", response_model=dict)
async def remove_member_groups(
        slug: str,
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("member_groups_write")),
        db: AsyncSession = Depends(get_db)
):
    member_groups_repository = SQLMemberGroupsRepository(db)
    member_groups_service = MemberGroupUseCases(member_groups_repository)
    member_group = await member_groups_service.delete_member_groups(slug, current_user)
    if member_group is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Member Group Delete Unsuccessful")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": []
    }
