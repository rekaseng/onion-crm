from abc import ABC, abstractmethod
from typing import Optional, List
from domain.models.machine_contracts import MachineContracts, MachineContractsBase


class MachineContractsRepository(ABC):
    @abstractmethod
    async def add(self, machine_contracts: MachineContracts, current_user: dict) -> bool:
        pass

    @abstractmethod
    async def get_by_id(self, id: int, current_user: dict) -> Optional[MachineContracts]:
        pass

    @abstractmethod
    async def get_by_tenant_id(self, current_user: dict) -> Optional[MachineContracts]:
        pass

    @abstractmethod
    async def get_all(self, current_user: dict) -> List[MachineContracts]:
        pass

    @abstractmethod
    async def update_machine_contracts(self, id: int, machine_contracts_update_dto: MachineContractsBase, current_user: dict) -> bool:
        pass

    @abstractmethod
    async def delete_machine_contracts(self, id: int, current_user: dict) -> bool:
        pass