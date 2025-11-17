from typing import List

from domain.models.machines import Machines, MachinesBase
from domain.repositories.machines_repository import MachinesRepository
from datetime import datetime


class MachinesUseCases:
    def __init__(self, machines_repository: MachinesRepository):
        self.machines_repository = machines_repository

    async def add(self, machines_dto: MachinesBase, current_user: dict) -> bool:
        machines = Machines(
            created_at=datetime.now(),
            updated_at=datetime.now(),
            name=machines_dto.name,
            is_active=True,
            is_deleted=False,
            deleted_at=None,
            created_by=current_user["user"].id,
            updated_by=current_user["user"].id,
            deleted_by=None
        )
        await self.machines_repository.add(machines, current_user)
        return machines

    async def get_all(self, current_user: dict) -> List[Machines]:
        machines = await self.machines_repository.get_all(current_user)
        return machines

    async def get_by_id(self, id: int, current_user: dict) -> Machines:
        machines = await self.machines_repository.get_by_id(id, current_user)
        return machines

    async def update_machines(self, id:int, machines_update_dto: MachinesBase, current_user: dict) -> bool:
        machines = await self.machines_repository.update_machines(id, machines_update_dto, current_user)
        return machines

    async def delete_machines(self, id: int, current_user: dict) -> bool:
        machines = await self.machines_repository.delete_machines(int, current_user)
        return machines
