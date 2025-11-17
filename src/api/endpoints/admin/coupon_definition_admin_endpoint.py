from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from api.deps import get_db, get_current_user, check_permission, get_admin, get_current_user_auth
from fastapi import HTTPException
from typing import List
from application.dto.auth_dto import UserAuthDTO
from application.use_cases.coupon_definition_use_cases import CouponDefinitionUseCases
from domain.models.coupon_definition import CouponDefinitionBase
from infrastructure.repositories.sql_coupon_definition_repository import SQLCouponDefinitionRepository


router = APIRouter()


@router.post("/", response_model=dict)
async def coupon_definition_add(
        coupon_dto: CouponDefinitionBase,
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        permission: bool = Depends(check_permission("coupon_definition_write")),
        is_admin: bool = Depends(get_admin),
        db: AsyncSession = Depends(get_db)
):

    coupon_repository = SQLCouponDefinitionRepository(db)
    coupon_definition_service = CouponDefinitionUseCases(coupon_repository)
    user_id = current_user.user.id
    tenant_id = current_user.tenant.id
    new_coupon = await coupon_definition_service.add(coupon_dto, user_id,  tenant_id)
    if new_coupon is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error Creating Coupon Definition")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": new_coupon
    }


@router.get("/", response_model=dict)
async def get_admin_coupon_definitions(
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        permission: bool = Depends(check_permission("coupon_definition_read")),
        is_admin: bool = Depends(get_admin),
        db: AsyncSession = Depends(get_db)
):
    coupon_repository = SQLCouponDefinitionRepository(db)
    coupon_service = CouponDefinitionUseCases(coupon_repository)
    coupons = await coupon_service.get_all()
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": {"items": coupons}
    }


@router.get("/{id}", response_model=dict)
async def get_admin_coupon_definition(
        id: int,
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        permission: bool = Depends(check_permission("coupon_definition_read")),
        is_admin: bool = Depends(get_admin),
        db: AsyncSession = Depends(get_db)
):
    coupon_repository = SQLCouponDefinitionRepository(db)
    coupon_service = CouponDefinitionUseCases(coupon_repository)
    coupon = await coupon_service.get_by_id(id)
    return {
         "error_message": None,
         "success": True,
         "error_code": None,
         "result": coupon
    }


@router.put("/{id}", response_model=dict)
async def admin_coupon_definition_update(
        id:int,
        coupon_update_dto: CouponDefinitionBase,
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        permission: bool = Depends(check_permission("coupon_definition_write")),
        is_admin: bool = Depends(get_admin),
        db: AsyncSession = Depends(get_db)
):
    coupon_repository = SQLCouponDefinitionRepository(db)
    coupon_service = CouponDefinitionUseCases(coupon_repository)
    coupon = await coupon_service.update_coupon_definition(id, coupon_update_dto, current_user.user.id)
    if coupon is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Coupon Definition Update Unsuccessful")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": coupon
    }


@router.delete("/{id}", response_model=dict)
async def remove_admin_coupon_definition(
        id: int,
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        permission: bool = Depends(check_permission("coupon_definition_write")),
        is_admin: bool = Depends(get_admin),
        db: AsyncSession = Depends(get_db)
):
    coupon_repository = SQLCouponDefinitionRepository(db)
    coupon_service = CouponDefinitionUseCases(coupon_repository)
    result = await coupon_service.delete_coupon_definition(id, current_user.user.id)
    if result is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Coupon Definition Delete Unsuccessful")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": result
    }

