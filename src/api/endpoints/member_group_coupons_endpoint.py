from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from domain.models.member_group_coupon import MemberGroupCouponBase
from api.deps import get_db, get_current_user, check_permission
from application.use_cases.member_group_coupons_use_cases import MemberGroupCouponsUseCases
from infrastructure.repositories.sql_member_group_coupons_repository import SQLMemberGroupCouponsRepository
from fastapi import HTTPException
from typing import List

router = APIRouter()


@router.post("/", response_model=dict)
async def member_group_coupons_add(
        member_group_coupons_dto: MemberGroupCouponBase,
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("member_groups_write")),
        db: AsyncSession = Depends(get_db)
):
    member_group_coupons_repository = SQLMemberGroupCouponsRepository(db)
    member_group_coupons_service = MemberGroupCouponsUseCases(member_group_coupons_repository)
    new_member_group_coupons = await member_group_coupons_service.add(member_group_coupons_dto, current_user)
    if new_member_group_coupons is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong Member Group Coupon")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": [new_member_group_coupons]
    }


@router.get("/", response_model=dict)
async def get_member_group_coupons(
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("member_groups_read")),
        db: AsyncSession = Depends(get_db)
):
    member_group_coupons_repository = SQLMemberGroupCouponsRepository(db)
    member_group_coupons_service = MemberGroupCouponsUseCases(member_group_coupons_repository)
    member_group_coupons = await member_group_coupons_service.get_all(current_user)
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": {"items": member_group_coupons}
    }


@router.get("/{member_group_id}", response_model=dict)
async def get_member_group_coupons(
        member_group_id: int,
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("member_groups_read")),
        db: AsyncSession = Depends(get_db)
):
    member_group_coupons_repository = SQLMemberGroupCouponsRepository(db)
    member_group_coupons_service = MemberGroupCouponsUseCases(member_group_coupons_repository)
    member_group_coupons = await member_group_coupons_service.get_by_member_group_id(member_group_id, current_user)
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
            "result": member_group_coupons
    }



@router.put("/{member_group_coupon_id}", response_model=dict)
async def member_group_coupons_update(
        member_group_coupons_update_dto: MemberGroupCouponBase,
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("member_groups_write")),
        db: AsyncSession = Depends(get_db)
):
    member_group_coupons_repository = SQLMemberGroupCouponsRepository(db)
    member_group_coupons_service = MemberGroupCouponsUseCases(member_group_coupons_repository)
    member_group_coupon = await member_group_coupons_service.update_member_group_coupons(member_group_coupons_update_dto, current_user)
    if member_group_coupon is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Member Group Coupon Update Unsuccessful")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": []
    }


@router.delete("/{member_group_coupon_id}", response_model=dict)
async def remove_member_group_coupons(
        member_group_coupon_id: int,
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("member_groups_write")),
        db: AsyncSession = Depends(get_db)
):
    member_group_coupons_repository = SQLMemberGroupCouponsRepository(db)
    member_group_coupons_service = MemberGroupCouponsUseCases(member_group_coupons_repository)
    member_group_coupon = await member_group_coupons_service.delete_member_group_coupons(member_group_coupon_id, current_user)
    if member_group_coupon is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Member Group Coupon Delete Unsuccessful")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": []
    }
