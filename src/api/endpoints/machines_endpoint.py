from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse

from domain.models.machines import MachinesBase
from api.deps import get_db, get_current_user, check_permission
from application.use_cases.machines_use_cases import MachinesUseCases
from infrastructure.repositories.sql_machines_repository import SQLMachinesRepository
from db_error_handlers import handle_db_errors

router = APIRouter()

@router.post("/", response_model=dict)
@handle_db_errors
async def machines_add(
        machines_dto: MachinesBase,
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("machines_write")),
        db: AsyncSession = Depends(get_db)
):
    machines_repository = SQLMachinesRepository(db)
    machines_service = MachinesUseCases(machines_repository)
    new_machines = await machines_service.add(machines_dto, current_user, permission)
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": [new_machines.dict()]
    }


@router.get("/", response_model=dict)
@handle_db_errors
async def get_machines(
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("machines_read")),
        db: AsyncSession = Depends(get_db)
):
    machines_repository = SQLMachinesRepository(db)
    machines_service = MachinesUseCases(machines_repository)
    machines = await machines_service.get_all(current_user, permission)
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": {"items": machines}
    }


@router.get("/{machines}", response_model=dict)
@handle_db_errors
async def get_machines(
        name: str,
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("machines_read")),
        db: AsyncSession = Depends(get_db)
):
    machines_repository = SQLMachinesRepository(db)
    machines_service = MachinesUseCases(machines_repository)
    machines = await machines_service.get_by_name(name, current_user, permission)
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": machines
    }


@router.put("/{machines}", response_model=dict)
@handle_db_errors
async def machines_update(
        machines_update_dto: MachinesBase,
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("machines_write")),
        db: AsyncSession = Depends(get_db)
):
    machines_repository = SQLMachinesRepository(db)
    machines_service = MachinesUseCases(machines_repository)
    await machines_service.update_machines(machines_update_dto, current_user, permission)
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": []
    }


@router.delete("/{machines}", response_model=dict)
@handle_db_errors
async def remove_machines(
        name: str,
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("machines_write")),
        db: AsyncSession = Depends(get_db)
):
    machines_repository = SQLMachinesRepository(db)
    machines_service = MachinesUseCases(machines_repository)
    await machines_service.delete_machines(name, current_user, permission)
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": []
    }
