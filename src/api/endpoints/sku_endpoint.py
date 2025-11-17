from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from domain.models.sku import SkuBase
from api.deps import get_db, get_current_user, check_permission, get_current_user_auth
from application.use_cases.sku_use_cases import SkuUseCases
from infrastructure.repositories.sql_sku_repository import SQLSkuRepository
from fastapi import HTTPException
from typing import List
from application.dto.auth_dto import UserAuthDTO


router = APIRouter()


@router.post("/", response_model=dict)
async def sku_add(
        sku_dto: SkuBase,
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        permission: bool = Depends(check_permission("sku_write")),
        db: AsyncSession = Depends(get_db)
):
    sku_repository = SQLSkuRepository(db)
    sku_service = SkuUseCases(sku_repository)
    new_sku = await sku_service.add(sku_dto, current_user.user.id)
    if new_sku is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong Sku")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": []
    }


@router.get("/", response_model=dict)
async def get_skus(
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        permission: bool = Depends(check_permission("sku_read")),
        db: AsyncSession = Depends(get_db)
):
    sku_repository = SQLSkuRepository(db)
    sku_service = SkuUseCases(sku_repository)
    skus = await sku_service.get_all()
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": {"items": skus}
    }


@router.get("/{id}", response_model=dict)
async def get_sku(
        id: int,
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        permission: bool = Depends(check_permission("sku_read")),
        db: AsyncSession = Depends(get_db)
):
    sku_repository = SQLSkuRepository(db)
    sku_service = SkuUseCases(sku_repository)
    sku = await sku_service.get_by_id(id)
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": sku
    }


@router.put("/{id}", response_model=dict)
async def sku_update(
        id: int,
        sku_update_dto: SkuBase,
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        permission: bool = Depends(check_permission("sku_write")),
        db: AsyncSession = Depends(get_db)
):
    sku_repository = SQLSkuRepository(db)
    sku_service = SkuUseCases(sku_repository)
    sku = await sku_service.update_sku(id, sku_update_dto, current_user.user.id)
    if sku is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sku Update Unsuccessful")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": []
    }


@router.delete("/{id}", response_model=dict)
async def remove_sku(
        id: int,
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        permission: bool = Depends(check_permission("sku_write")),
        db: AsyncSession = Depends(get_db)
):
    sku_repository = SQLSkuRepository(db)
    sku_service = SkuUseCases(sku_repository)
    sku = await sku_service.delete_sku(id, current_user.user.id)
    if sku is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sku Delete Unsuccessful")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": []
    }
