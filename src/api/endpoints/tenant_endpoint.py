from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from domain.models.tenant import TenantBase
from api.deps import get_db, get_current_user, check_permission
from application.use_cases.tenant_use_cases import TenantUseCases
from infrastructure.repositories.sql_tenant_repository import SQLTenantRepository
from fastapi import HTTPException
from typing import List

router = APIRouter()


@router.post("/", response_model=dict)
async def tenant_add(
        tenant_dto: TenantBase,
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("tenant_write")),
        db: AsyncSession = Depends(get_db)
):
    tenant_repository = SQLTenantRepository(db)
    tenant_service = TenantUseCases(tenant_repository)
    new_tenant = await tenant_service.add(tenant_dto, current_user)
    if new_tenant is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong Tenant")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": new_tenant
    }


@router.get("/", response_model=dict)
async def get_tenants(
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("tenant_read")),
        db: AsyncSession = Depends(get_db)
):
    tenant_repository = SQLTenantRepository(db)
    tenant_service = TenantUseCases(tenant_repository)
    tenants = await tenant_service.get_all(current_user)
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": {"items": tenants}
    }


@router.get("/{id}", response_model=dict)
async def get_tenant(
        id: int,
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("tenant_read")),
        db: AsyncSession = Depends(get_db)
):
    tenant_repository = SQLTenantRepository(db)
    tenant_service = TenantUseCases(tenant_repository)
    tenant = await tenant_service.get_by_id(id, current_user)
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": tenant
    }


@router.put("/{id}", response_model=dict)
async def tenant_update(
        id: int,
        tenant_update_dto: TenantBase,
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("tenant_write")),
        db: AsyncSession = Depends(get_db)
):
    tenant_repository = SQLTenantRepository(db)
    tenant_service = TenantUseCases(tenant_repository)
    tenant = await tenant_service.update_tenant(id, tenant_update_dto, current_user)
    if tenant is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tenant Update Unsuccessful")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": []
    }


@router.delete("/{id}", response_model=dict)
async def remove_tenant(
        id: int,
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("tenant_write")),
        db: AsyncSession = Depends(get_db)
):
    tenant_repository = SQLTenantRepository(db)
    tenant_service = TenantUseCases(tenant_repository)
    tenant = await tenant_service.delete_tenant(id, current_user)
    if tenant is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tenant Delete Unsuccessful")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": []
    }
