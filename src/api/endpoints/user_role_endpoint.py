from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from api.deps import get_db, get_current_user, check_permission
from application.use_cases.user_role_use_cases import UserRoleUseCases
from infrastructure.repositories.sql_user_role_repository import SQLUserRoleRepository
from domain.models.user_role import UserRoleBase
from fastapi import HTTPException
from typing import List

router = APIRouter()


@router.get("/", response_model=dict)
async def get_user_roles(
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("user_role_read")),
        db: AsyncSession = Depends(get_db)
):
    user_role_repository = SQLUserRoleRepository(db)
    user_role_service = UserRoleUseCases(user_role_repository)
    user_roles = await user_role_service.get_all(current_user)
    if not user_roles:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong User Role")

    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": {"items": user_roles}
    }


@router.get("/{user_role}", response_model=dict)
async def get_user_role(
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("user_role_read")),
        db: AsyncSession = Depends(get_db)
):
    user_role_repository = SQLUserRoleRepository(db)
    user_role_service = UserRoleUseCases(user_role_repository)
    user_role = await user_role_service.get_by_user_id(current_user)
    if not user_role:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong User Role")

    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": user_role
    }


@router.put("/{user_role}", response_model=dict)
async def user_role_update(
        id: int,
        update_user_role_dto: UserRoleBase,
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("user_role_write")),
        db: AsyncSession = Depends(get_db)
):
    user_role_repository = SQLUserRoleRepository(db)
    user_role_service = UserRoleUseCases(user_role_repository)
    user_role = await user_role_service.update_user_role(id, update_user_role_dto, current_user)
    if user_role:
        return {
            "error_message": None,
            "success": True,
            "error_code": None,
            "result": []
        }
    else:
        raise HTTPException(status_code=400, detail="Wrong User Role")