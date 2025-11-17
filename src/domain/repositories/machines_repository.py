from abc import ABC, abstractmethod
from typing import Optional, List
from domain.models.machines import Machines, MachinesBase


class MachinesRepository(ABC):
    @abstractmethod
    async def add(self, machines: Machines, current_user: dict) -> bool:
        pass

    @abstractmethod
    async def get_by_id(self, id: int, current_user: dict) -> Optional[Machines]:
        pass

    @abstractmethod
    async def get_all(self, current_user: dict) -> List[Machines]:
        pass

    @abstractmethod
    async def update_machines(self, id: int, machines_update_dto: MachinesBase, current_user: dict) -> bool:
        pass

    @abstractmethod
    async def delete_machines(self, id: int, current_user: dict) -> bool:
        pass