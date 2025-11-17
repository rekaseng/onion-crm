from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from domain.models.coupon import CouponBase, Coupon
from api.deps import get_db, get_current_user, check_permission, get_current_user_auth
from application.use_cases.coupon_use_cases import CouponUseCases
from infrastructure.repositories.sql_coupon_repository import SQLCouponRepository
from fastapi import HTTPException
from typing import List
from application.dto.auth_dto import UserAuthDTO

router = APIRouter()


@router.post("/", response_model=dict)
async def coupon_add(
        coupon_dto: CouponBase,
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        permission: bool = Depends(check_permission("coupon_write")),
        db: AsyncSession = Depends(get_db)
):
    coupon_repository = SQLCouponRepository(db)
    coupon_service = CouponUseCases(coupon_repository)
    new_coupon = await coupon_service.add(coupon_dto)
    if new_coupon is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong Coupon")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": [new_coupon]
    }


@router.get("/", response_model=dict)
async def get_coupons(
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        permission: bool = Depends(check_permission("coupon_read")),
        db: AsyncSession = Depends(get_db)
):
    coupon_repository = SQLCouponRepository(db)
    coupon_service = CouponUseCases(coupon_repository)
    coupons = await coupon_service.get_all()
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": {"items": coupons}
    }


@router.get("/{id}", response_model=dict)
async def get_coupon(
        id: int,
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        permission: bool = Depends(check_permission("coupon_read")),
        db: AsyncSession = Depends(get_db)
):
    coupon_repository = SQLCouponRepository(db)
    coupon_service = CouponUseCases(coupon_repository)
    coupon = await coupon_service.get_by_id(id)
    return {
         "error_message": None,
         "success": True,
         "error_code": None,
         "result": coupon
    }


@router.put("/{id}", response_model=dict)
async def coupon_update(
        id: int,
        coupon_update_dto: CouponBase,
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        permission: bool = Depends(check_permission("coupon_write")),
        db: AsyncSession = Depends(get_db)
):
    coupon_repository = SQLCouponRepository(db)
    coupon_service = CouponUseCases(coupon_repository)
    coupon = await coupon_service.update_coupon(id, coupon_update_dto, current_user.user.id)
    if coupon is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Coupon Update Unsuccessful")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": []
    }


@router.delete("/{id}", response_model=dict)
async def remove_coupon(
        id: int,
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        permission: bool = Depends(check_permission("coupon_write")),
        db: AsyncSession = Depends(get_db)
):
    coupon_repository = SQLCouponRepository(db)
    coupon_service = CouponUseCases(coupon_repository)
    coupon = await coupon_service.delete_coupon(id, current_user.user.id)
    if coupon is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Coupon Delete Unsuccessful")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": []
    }
