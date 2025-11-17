from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from domain.models.machine_contracts import MachineContractsBase
from api.deps import get_db, get_current_user, check_permission
from application.use_cases.machine_contracts_use_cases import MachineContractsUseCases
from infrastructure.repositories.sql_machine_contracts_repository import SQLMachineContractsRepository
from db_error_handlers import handle_db_errors

router = APIRouter()


@router.post("/", response_model=dict)
@handle_db_errors
async def machine_contracts_add(
        machine_contracts_dto: MachineContractsBase,
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("machine_contracts_write")),
        db: AsyncSession = Depends(get_db)
):
    machine_contracts_repository = SQLMachineContractsRepository(db)
    machine_contracts_service = MachineContractsUseCases(machine_contracts_repository)
    new_machine_contracts = await machine_contracts_service.add(machine_contracts_dto, current_user, permission)
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": new_machine_contracts
    }


@router.get("/", response_model=dict)
@handle_db_errors
async def get_machine_contracts(
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("machine_contracts_read")),
        db: AsyncSession = Depends(get_db)
):
    machine_contracts_repository = SQLMachineContractsRepository(db)
    machine_contracts_service = MachineContractsUseCases(machine_contracts_repository)
    machine_contracts = await machine_contracts_service.get_all(current_user, permission)
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": [machine_contracts.dict() for machine_contracts in machine_contracts]
    }


@router.get("/{machine_contracts}", response_model=dict)
@handle_db_errors
async def get_machine_contracts(
        name: str,
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("machine_contracts_read")),
        db: AsyncSession = Depends(get_db)
):
    machine_contracts_repository = SQLMachineContractsRepository(db)
    machine_contracts_service = MachineContractsUseCases(machine_contracts_repository)
    machine_contracts = await machine_contracts_service.get_by_name(name, current_user, permission)
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": machine_contracts
    }


@router.put("/{machine_contracts}", response_model=dict)
@handle_db_errors
async def machine_contracts_update(
        machine_contracts_update_dto: MachineContractsBase,
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("machine_contracts_write")),
        db: AsyncSession = Depends(get_db)
):
    machine_contracts_repository = SQLMachineContractsRepository(db)
    machine_contracts_service = MachineContractsUseCases(machine_contracts_repository)
    await machine_contracts_service.update_machine_contracts(machine_contracts_update_dto, current_user, permission)
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": []
    }


@router.delete("/{machine_contracts}", response_model=dict)
@handle_db_errors
async def remove_machine_contracts(
        name: str,
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("machine_contracts_write")),
        db: AsyncSession = Depends(get_db)
):
    machine_contracts_repository = SQLMachineContractsRepository(db)
    machine_contracts_service = MachineContractsUseCases(machine_contracts_repository)
    await machine_contracts_service.delete_machine_contracts(name, current_user, permission)
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": []
    }
