from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from domain.models.role import RoleBase
from api.deps import get_db, get_current_user, check_permission, get_admin
from application.use_cases.role_use_cases import RoleUseCases
from infrastructure.repositories.sql_role_repository import SQLRoleRepository
from typing import List

router = APIRouter()

@router.post("/", response_model=dict)
async def role_admin_add(
        role_dto: RoleBase,
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("role_write")),
        is_admin: bool = Depends(get_admin),
        db: AsyncSession = Depends(get_db)
):
    role_repository = SQLRoleRepository(db)
    role_service = RoleUseCases(role_repository)
    new_role = await role_service.add_admin(role_dto, current_user)
    if new_role is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong Role")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": new_role
    }

@router.get("/", response_model=dict)
async def get_roles_admin(
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("role_read")),
        is_admin: bool = Depends(get_admin),
        db: AsyncSession = Depends(get_db)
):
    role_repository = SQLRoleRepository(db)
    role_service = RoleUseCases(role_repository)
    roles = await role_service.get_all_admin(current_user)
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": {"items" :roles}
    }

@router.get("/{role_id}", response_model=dict)
async def get_role_admin(
        role_id: int,
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("role_read")),
        is_admin: bool = Depends(get_admin),
        db: AsyncSession = Depends(get_db)
):
    role_repository = SQLRoleRepository(db)
    role_service = RoleUseCases(role_repository)
    role = await role_service.get_by_id(role_id, current_user)
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": role
    }

@router.put("/{role_id}", response_model=dict)
async def role_admin_update(
        role_id: int,
        update_role_dto: RoleBase,
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("role_write")),
        is_admin: bool = Depends(get_admin),
        db: AsyncSession = Depends(get_db)
):
    role_repository = SQLRoleRepository(db)
    role_service = RoleUseCases(role_repository)
    role = await role_service.update_role_admin(role_id, update_role_dto, current_user)
    if role is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Role Update Unsuccessful")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": []
    }

@router.delete("/{role_id}", response_model=dict)
async def remove_role_admin(
        role_id: int,
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("role_write")),
        is_admin: bool = Depends(get_admin),
        db: AsyncSession = Depends(get_db)
):
    role_repository = SQLRoleRepository(db)
    role_service = RoleUseCases(role_repository)
    role = await role_service.delete_role_admin(role_id, current_user)
    if role is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Role Delete Unsuccessful")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": []
    }
