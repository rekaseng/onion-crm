from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from api.deps import get_db, get_current_user, check_permission, get_admin, get_current_user_auth
from fastapi import HTTPException
from typing import List

from api.di import get_user_coupon_use_cases
from application.dto.auth_dto import UserAuthDTO
from domain.models.user_coupon import UserCouponBase
from infrastructure.repositories.sql_coupon_definition_repository import SQLCouponDefinitionRepository
from infrastructure.repositories.sql_user_coupon_repository import SQLUserCouponRepository
from application.use_cases.user_coupon_use_cases import UserCouponUseCases


router = APIRouter()


@router.post("/", response_model=dict)
async def user_coupon_add(
        coupon_dto: UserCouponBase,
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        permission: bool = Depends(check_permission("user_coupon_write")),
        is_admin: bool = Depends(get_admin),
        db: AsyncSession = Depends(get_db),
        user_coupon_use_cases: UserCouponUseCases = Depends(get_user_coupon_use_cases)

):

    user_id = current_user.user.id
    new_coupon = await user_coupon_use_cases.add(coupon_dto, user_id)
    if new_coupon is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong User Coupon")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": new_coupon
    }


@router.get("/", response_model=dict)
async def get_admin_user_coupons(
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        permission: bool = Depends(check_permission("user_coupon_read")),
        is_admin: bool = Depends(get_admin),
        db: AsyncSession = Depends(get_db),
        user_coupon_use_cases: UserCouponUseCases = Depends(get_user_coupon_use_cases)
):
    coupons = await user_coupon_use_cases.get_all()
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": {"items": coupons}
    }


@router.get("/{id}", response_model=dict)
async def get_admin_user_coupon(
        id: int,
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        permission: bool = Depends(check_permission("user_coupon_read")),
        is_admin: bool = Depends(get_admin),
        db: AsyncSession = Depends(get_db),
        user_coupon_use_cases: UserCouponUseCases = Depends(get_user_coupon_use_cases)
):
    coupon = await user_coupon_use_cases.get_by_id(id)
    return {
         "error_message": None,
         "success": True,
         "error_code": None,
         "result": coupon
    }


@router.put("/{id}", response_model=dict)
async def admin_user_coupon_update(
        id:int,
        coupon_update_dto: UserCouponBase,
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        permission: bool = Depends(check_permission("user_coupon_write")),
        is_admin: bool = Depends(get_admin),
        db: AsyncSession = Depends(get_db),
        user_coupon_use_cases: UserCouponUseCases = Depends(get_user_coupon_use_cases)

):
    coupon = await user_coupon_use_cases.update_user_coupon(id, coupon_update_dto, current_user.user.id)
    if coupon is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User Coupon Update Unsuccessful")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": coupon
    }


@router.delete("/{id}", response_model=dict)
async def remove_admin_user_coupon(
        id: int,
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        permission: bool = Depends(check_permission("user_coupon_write")),
        is_admin: bool = Depends(get_admin),
        db: AsyncSession = Depends(get_db),
        user_coupon_use_cases: UserCouponUseCases = Depends(get_user_coupon_use_cases)
):
    result = await user_coupon_use_cases.delete_user_coupon(id, current_user.user.id)
    if result is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User Coupon Delete Unsuccessful")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": result
    }

