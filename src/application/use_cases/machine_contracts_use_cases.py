from typing import List

from domain.models.machine_contracts import MachineContracts, MachineContractsBase
from domain.repositories.machine_contracts_repository import MachineContractsRepository
from datetime import datetime


class MachineContractsUseCases:
    def __init__(self, machine_contracts_repository: MachineContractsRepository):
        self.machine_contracts_repository = machine_contracts_repository

    async def add(self, machine_contracts_dto: MachineContractsBase, current_user: dict) -> bool:
        machine_contracts = MachineContracts(
            created_at=datetime.now(),
            updated_at=datetime.now(),
            start_date=machine_contracts_dto.start_date,
            end_date=machine_contracts_dto.end_date,
            name=machine_contracts_dto.name,
            machine_id=None,
            tenant_id=current_user["tenant"].id,
            is_deleted=False,
            deleted_at=None,
            created_by=current_user["user"].id,
            updated_by=current_user["user"].id,
            deleted_by=None
        )
        machine_contracts = await self.machine_contracts_repository.add(machine_contracts, current_user)
        return machine_contracts

    async def get_all(self, current_user: dict) -> List[MachineContracts]:
        machine_contracts = await self.machine_contracts_repository.get_all(current_user)
        return machine_contracts

    async def get_by_id(self, id: int, current_user: dict) -> MachineContracts:
        machine_contracts = await self.machine_contracts_repository.get_by_id(id, current_user)
        return machine_contracts

    async def get_by_tenant_id(self, current_user: dict) -> MachineContracts:
        machine_contracts = await self.machine_contracts_repository.get_by_tenant_id(current_user)
        return machine_contracts

    async def update_machine_contracts(self, id:int, machine_contracts_update_dto: MachineContractsBase, current_user: dict) -> bool:
        machine_contracts = await self.machine_contracts_repository.update_machine_contracts(id, machine_contracts_update_dto, current_user)
        return machine_contracts

    async def delete_machine_contracts(self, id: int, current_user: dict) -> bool:
        machine_contracts = await self.machine_contracts_repository.delete_machine_contracts(id, current_user)
        return machine_contracts
