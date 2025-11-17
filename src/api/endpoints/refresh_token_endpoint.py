from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from domain.models.refresh_token import RefreshTokenBase
from api.deps import get_db, get_current_user
from application.use_cases.refresh_token_use_cases import RefreshTokenUseCases
from infrastructure.repositories.sql_refresh_token_repository import SQLRefreshTokenRepository
from fastapi import HTTPException
from typing import List

router = APIRouter()


@router.post("/", response_model=dict)
async def refresh_token_add(
        refresh_token_dto: RefreshTokenBase,
        db: AsyncSession = Depends(get_db)
):
    refresh_token_repository = SQLRefreshTokenRepository(db)
    refresh_token_service = RefreshTokenUseCases(refresh_token_repository)
    new_refresh_token = await refresh_token_service.add(refresh_token_dto)
    if new_refresh_token is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong Refresh Token")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": new_refresh_token
    }


@router.get("/", response_model=dict)
async def get_refresh_tokens(
        db: AsyncSession = Depends(get_db)
):
    refresh_token_repository = SQLRefreshTokenRepository(db)
    refresh_token_service = RefreshTokenUseCases(refresh_token_repository)
    refresh_tokens = await refresh_token_service.get_all()
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": {"refresh tokens": refresh_tokens}

    }


@router.get("/{id}", response_model=dict)
async def get_refresh_token(
        id: int,
        db: AsyncSession = Depends(get_db)
):
    refresh_token_repository = SQLRefreshTokenRepository(db)
    refresh_token_service = RefreshTokenUseCases(refresh_token_repository)
    refresh_token = await refresh_token_service.get_by_refresh_token(id)
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": refresh_token
    }


@router.put("/{id}", response_model=dict)
async def refresh_token_update(
        update_refresh_token_dto: RefreshTokenBase,
        db: AsyncSession = Depends(get_db)
):
    refresh_token_repository = SQLRefreshTokenRepository(db)
    refresh_token_service = RefreshTokenUseCases(refresh_token_repository)
    refresh_token = await refresh_token_service.update_refresh_token(update_refresh_token_dto)
    if refresh_token is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Refresh Token Update Unsuccessful")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": []
    }


@router.delete("/{id}", response_model=dict)
async def remove_refresh_token(
        id: int,
        db: AsyncSession = Depends(get_db)
):
    refresh_token_repository = SQLRefreshTokenRepository(db)
    refresh_token_service = RefreshTokenUseCases(refresh_token_repository)
    refresh_token = await refresh_token_service.delete_refresh_token(id)
    if refresh_token is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Refresh Token Delete Unsuccessful")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": []
    }
