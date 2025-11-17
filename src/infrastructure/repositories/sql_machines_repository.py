from typing import List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from domain.models.machines import Machines, MachinesBase
from domain.repositories.machines_repository import MachinesRepository
from infrastructure.orm.machines_orm_model import MachinesOrmModel
from fastapi import HTTPException
from datetime import datetime

from infrastructure.orm.orm_update_helper import update_orm_model_from_domain


class SQLMachinesRepository(MachinesRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all(self, current_user: dict) -> List[Machines]:
        result = await self.db_session.execute(select(MachinesOrmModel).filter(MachinesOrmModel.is_deleted.is_(False)))
        orm_machines = result.scalars().all()
        machines = [item.to_domain() for item in orm_machines]
        return machines

    async def add(self, machines: Machines, current_user: dict) -> bool:
        result = await self.db_session.execute(select(MachinesOrmModel).filter_by(name=machines.name))
        orm_machines = result.scalars().first()

        if orm_machines:
            raise HTTPException(status_code=400, detail="Product with this machines already exists")

        orm_machines = MachinesOrmModel.from_domain(machines)
        await self.db_session.merge(orm_machines)
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False

    async def get_by_id(self, id: str, current_user: dict) -> Machines:
        result = await self.db_session.execute(select(MachinesOrmModel).filter(MachinesOrmModel.id == id,
                                                                               MachinesOrmModel.is_deleted.is_(False)))
        orm_machines = result.scalars().first()

        if orm_machines is None:
            raise HTTPException(status_code=400, detail="Wrong Machines")

        machines = orm_machines.to_domain()
        return machines

    async def update_machines(self, id: int, update_machines: MachinesBase, current_user: dict) -> bool:
        result = await self.db_session.execute(select(MachinesOrmModel).filter(MachinesOrmModel.id == id,
                                                                               MachinesOrmModel.is_deleted.is_(False)))
        orm_machines = result.scalars().first()

        if orm_machines is None:
            raise HTTPException(status_code=400, detail="Wrong Machines")

        orm_machines = update_orm_model_from_domain(orm_machines, update_machines)
        orm_machines.updated_at = datetime.now()
        orm_machines.updated_by = current_user["user"].id
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False

    async def delete_machines(self, id: int, current_user: dict) -> bool:
        result = await self.db_session.execute(select(MachinesOrmModel).filter(MachinesOrmModel.id == id,
                                                                               MachinesOrmModel.is_deleted.is_(False)))
        orm_machines = result.scalars().first()

        if orm_machines is None:
            raise HTTPException(status_code=400, detail="Wrong Machines")

        orm_machines.updated_at = datetime.now()
        orm_machines.is_deleted = True
        orm_machines.deleted_at = datetime.now()
        orm_machines.deleted_by = current_user["user"].id
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False