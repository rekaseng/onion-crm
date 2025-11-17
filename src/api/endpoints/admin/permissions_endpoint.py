from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.deps import get_db, get_current_user, check_permission, get_admin
from application.use_cases.permission_use_cases import PermissionUseCases
from infrastructure.repositories.sql_permission_repository import SQLPermissionRepository
from domain.models.permission import PermissionBase
from typing import List

router = APIRouter()


@router.get("/", response_model=dict)
async def get_all_permissions(
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("permissions_read")),
        is_admin: bool = Depends(get_admin),
        db: AsyncSession = Depends(get_db)
):
    permission_repository = SQLPermissionRepository(db)
    permission_service = PermissionUseCases(permission_repository)
    permissions = await permission_service.get_all()
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": {"items" :permissions}
    }
