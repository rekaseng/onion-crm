from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from domain.models.machine_contracts import MachineContractsBase
from api.deps import get_db, get_current_user, check_permission, get_hq_admin, get_admin
from application.use_cases.machine_contracts_use_cases import MachineContractsUseCases
from infrastructure.repositories.sql_machine_contracts_repository import SQLMachineContractsRepository
from fastapi import HTTPException
from typing import List

router = APIRouter()


@router.post("/", response_model=dict)
async def machine_contracts_add(
        machine_contracts_dto: MachineContractsBase,
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("machine_contracts_write")),
        is_hq_admin: bool = Depends(get_hq_admin),
        db: AsyncSession = Depends(get_db)
):
    machine_contracts_repository = SQLMachineContractsRepository(db)
    machine_contracts_service = MachineContractsUseCases(machine_contracts_repository)
    new_machine_contracts = await machine_contracts_service.add(machine_contracts_dto, current_user)
    if new_machine_contracts is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong Machine Contract")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": [new_machine_contracts]
    }


@router.get("/", response_model=dict)
async def get_machine_contracts(
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("machine_contracts_read")),
        is_hq_admin: bool = Depends(get_hq_admin),
        db: AsyncSession = Depends(get_db)
):
    machine_contracts_repository = SQLMachineContractsRepository(db)
    machine_contracts_service = MachineContractsUseCases(machine_contracts_repository)
    machine_contracts = await machine_contracts_service.get_all(current_user)
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": [machine_contracts]
    }


@router.get("/{machine_contracts_id}", response_model=dict)
async def get_machine_contract(
        id: int,
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("machine_contracts_read")),
        is_hq_admin: bool = Depends(get_hq_admin),
        db: AsyncSession = Depends(get_db)
):
    machine_contracts_repository = SQLMachineContractsRepository(db)
    machine_contracts_service = MachineContractsUseCases(machine_contracts_repository)
    machine_contracts = await machine_contracts_service.get_by_id(id, current_user)
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": {"items":machine_contracts}
    }


@router.get("/{tenant_id}", response_model=dict)
async def get_admin_machine_contracts(
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("machine_contracts_read")),
        is_admin: bool = Depends(get_admin),
        db: AsyncSession = Depends(get_db)
):
    machine_contracts_repository = SQLMachineContractsRepository(db)
    machine_contracts_service = MachineContractsUseCases(machine_contracts_repository)
    machine_contracts = await machine_contracts_service.get_by_tenant_id(current_user)
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": machine_contracts
    }


@router.put("/{id}", response_model=dict)
async def machine_contracts_update(
        id: int,
        machine_contracts_update_dto: MachineContractsBase,
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("machine_contracts_write")),
        is_hq_admin: bool = Depends(get_hq_admin),
        db: AsyncSession = Depends(get_db)
):
    machine_contracts_repository = SQLMachineContractsRepository(db)
    machine_contracts_service = MachineContractsUseCases(machine_contracts_repository)
    machine_contract = await machine_contracts_service.update_machine_contracts(id, machine_contracts_update_dto, current_user)
    if machine_contract is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Machine Contract Update Unsuccessful")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": []
    }


@router.delete("/{machine_contracts_id}", response_model=dict)
async def remove_machine_contracts(
        id: int,
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("machine_contracts_write")),
        is_hq_admin: bool = Depends(get_hq_admin),
        db: AsyncSession = Depends(get_db)
):
    machine_contracts_repository = SQLMachineContractsRepository(db)
    machine_contracts_service = MachineContractsUseCases(machine_contracts_repository)
    machine_contract = await machine_contracts_service.delete_machine_contracts(id, current_user)
    if machine_contract is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Machine Contract Delete Unsuccessful")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": []
    }
