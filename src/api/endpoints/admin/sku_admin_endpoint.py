from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from domain.models.coupon import CouponBase
from api.deps import get_db, get_current_user, check_permission, get_admin, get_current_user_auth
from fastapi import HTTPException
from typing import List
from application.dto.auth_dto import UserAuthDTO
from infrastructure.repositories.sql_sku_repository import SQLSkuRepository
from application.use_cases.sku_use_cases import SkuUseCases
from infrastructure.external.hq_adapter import HqAdapter


router = APIRouter()


@router.post("/update_skus", response_model=dict)
async def update_skus(
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        permission: bool = Depends(check_permission("sku_write")),
        db: AsyncSession = Depends(get_db)
):
    sku_repository = SQLSkuRepository(db)
    hq_adapter = HqAdapter()
    sku_service = SkuUseCases(sku_repository, hq_adapter)
    result = await sku_service.update_skus_from_hq()
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": result
    }