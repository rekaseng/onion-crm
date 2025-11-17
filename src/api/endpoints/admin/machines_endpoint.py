from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from domain.models.machines import MachinesBase
from api.deps import get_db, get_current_user, check_permission
from application.use_cases.machines_use_cases import MachinesUseCases
from infrastructure.repositories.sql_machines_repository import SQLMachinesRepository
from fastapi import HTTPException
from typing import List

router = APIRouter()


@router.post("/", response_model=dict)
async def machines_add(
        machines_dto: MachinesBase,
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("machines_write")),
        db: AsyncSession = Depends(get_db)
):
    machines_repository = SQLMachinesRepository(db)
    machines_service = MachinesUseCases(machines_repository)
    new_machines = await machines_service.add(machines_dto, current_user)
    if new_machines is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong Machines")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": [new_machines]
    }


@router.get("/", response_model=dict)
async def get_machines(
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("machines_read")),
        db: AsyncSession = Depends(get_db)
):
    machines_repository = SQLMachinesRepository(db)
    machines_service = MachinesUseCases(machines_repository)
    machines = await machines_service.get_all(current_user)
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": {"items": machines}
    }


@router.get("/{id}", response_model=dict)
async def get_machine(
        id: int,
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("machines_read")),
        db: AsyncSession = Depends(get_db)
):
    machines_repository = SQLMachinesRepository(db)
    machines_service = MachinesUseCases(machines_repository)
    machines = await machines_service.get_by_id(id, current_user)
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": machines
    }


@router.put("/{id}", response_model=dict)
async def machines_update(
        id: int,
        machines_update_dto: MachinesBase,
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("machines_write")),
        db: AsyncSession = Depends(get_db)
):
    machines_repository = SQLMachinesRepository(db)
    machines_service = MachinesUseCases(machines_repository)
    machines = await machines_service.update_machines(id, machines_update_dto, current_user)
    if machines is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Machines Update Unsuccessful")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": []
    }


@router.delete("/{id}", response_model=dict)
async def remove_machines(
        id: int,
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("machines_write")),
        db: AsyncSession = Depends(get_db)
):
    machines_repository = SQLMachinesRepository(db)
    machines_service = MachinesUseCases(machines_repository)
    machines = await machines_service.delete_machines(id, current_user)
    if machines is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Machines Delete Unsuccessful")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": []
    }