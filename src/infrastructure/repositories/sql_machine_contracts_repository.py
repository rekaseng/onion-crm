from typing import List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from domain.models.machine_contracts import MachineContracts, MachineContractsBase
from domain.repositories.machine_contracts_repository import MachineContractsRepository
from infrastructure.orm.machine_contracts_orm_model import MachineContractsOrmModel
from infrastructure.orm.machines_orm_model import MachinesOrmModel
from fastapi import HTTPException
from datetime import datetime

from infrastructure.orm.orm_update_helper import update_orm_model_from_domain


class SQLMachineContractsRepository(MachineContractsRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all(self, current_user: dict) -> List[MachineContracts]:
        result = await self.db_session.execute(
            select(MachineContractsOrmModel).filter(MachineContractsOrmModel.is_deleted.is_(False)))
        orm_machine_contracts = result.scalars().all()
        machine_contracts = [item.to_domain() for item in orm_machine_contracts]
        return machine_contracts

    async def add(self, machine_contracts: MachineContracts, current_user: dict) -> bool:
        machine_result = await self.db_session.execute(
            select(MachinesOrmModel).filter_by(name=machine_contracts.name))
        orm_machines = machine_result.scalars().first()

        if not orm_machines:
            raise HTTPException(status_code=400, detail="Wrong Machine")

        result = await self.db_session.execute(
            select(MachineContractsOrmModel).filter_by(name=machine_contracts.name))
        orm_machine_contracts = result.scalars().first()

        if orm_machine_contracts:
            raise HTTPException(status_code=400, detail="This machine_contracts already exists")

        # Set found machine_id to machine contract
        machine_contracts.machine_id = orm_machines.id
        orm_machine_contracts = MachineContractsOrmModel.from_domain(machine_contracts)
        await self.db_session.merge(orm_machine_contracts)
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False

    async def get_by_id(self, id: int, current_user: dict) -> MachineContracts:
        result = await self.db_session.execute(
            select(MachineContractsOrmModel).filter(MachineContractsOrmModel.id == id,
                                                    MachineContractsOrmModel.is_deleted.is_(False)))
        orm_machine_contracts = result.scalars().first()

        if orm_machine_contracts is None:
            raise HTTPException(status_code=400, detail="Wrong MachineContracts")

        machine_contracts = orm_machine_contracts.to_domain()
        return machine_contracts

    async def get_by_tenant_id(self, current_user: dict) -> MachineContracts:
        result = await self.db_session.execute(
            select(MachineContractsOrmModel).filter(MachineContractsOrmModel.tenant_id == current_user["tenant"].id,
                                                    MachineContractsOrmModel.is_deleted.is_(False)))
        orm_machine_contracts = result.scalars().first()

        if orm_machine_contracts is None:
            raise HTTPException(status_code=400, detail="Wrong MachineContracts")

        machine_contracts = orm_machine_contracts.to_domain()
        return machine_contracts

    async def update_machine_contracts(self, id: int, update_machine_contracts: MachineContractsBase, current_user: dict) -> bool:
        result = await self.db_session.execute(
            select(MachineContractsOrmModel).filter(MachineContractsOrmModel.id == id,
                                                    MachineContractsOrmModel.is_deleted.is_(False)))
        orm_machine_contracts = result.scalars().first()

        if orm_machine_contracts is None:
            raise HTTPException(status_code=400, detail="Wrong MachineContracts")

        orm_machine_contracts = update_orm_model_from_domain(orm_machine_contracts, update_machine_contracts)
        orm_machine_contracts.updated_at = datetime.now()
        orm_machine_contracts.updated_by = current_user["user"].id
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False

    async def delete_machine_contracts(self, id: int, current_user: dict) -> bool:
        result = await self.db_session.execute(
            select(MachineContractsOrmModel).filter(MachineContractsOrmModel.id == id,
                                                    MachineContractsOrmModel.is_deleted.is_(False)))
        orm_machine_contracts = result.scalars().first()

        if orm_machine_contracts is None:
            raise HTTPException(status_code=400, detail="Wrong MachineContracts")

        orm_machine_contracts.updated_at = datetime.now()
        orm_machine_contracts.is_deleted = True
        orm_machine_contracts.deleted_at = datetime.now()
        orm_machine_contracts.deleted_by = current_user["user"].id
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False
