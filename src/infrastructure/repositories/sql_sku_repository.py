from typing import List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from domain.models.sku import Sku, SkuBase
from domain.repositories.sku_repository import SkuRepository
from infrastructure.orm.sku_orm_model import SkuOrmModel
from fastapi import HTTPException
from datetime import datetime

from infrastructure.orm.orm_update_helper import update_orm_model_from_domain


class SQLSkuRepository(SkuRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all(self) -> List[Sku]:
        result = await self.db_session.execute(select(SkuOrmModel).filter(SkuOrmModel.is_deleted.is_(False)))
        orm_skus = result.scalars().all()
        skus = [item.to_domain() for item in orm_skus]
        return skus
    
    async def get_all_orm(self) -> List[SkuOrmModel]:
        result = await self.db_session.execute(select(SkuOrmModel))
        return result.scalars().all()

    async def add(self, sku: Sku) -> bool:
        result = await self.db_session.execute(select(SkuOrmModel).filter_by(sku=sku.sku))
        orm_sku = result.scalars().first()

        if orm_sku:
            raise HTTPException(status_code=400, detail="Product with this sku already exists")

        orm_sku = SkuOrmModel.from_domain(sku)
        await self.db_session.merge(orm_sku)
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False
        
    def add_none_commit(self, sku: SkuOrmModel):
        self.db_session.add(sku)
        
    async def commit(self) -> bool:
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError as e:
            print(f"Database error occurred: {e}")
            await self.db_session.rollback()
            return False

    async def get_by_id(self, id: int) -> Sku:
        result = await self.db_session.execute(select(SkuOrmModel).filter(SkuOrmModel.id == id, SkuOrmModel.is_deleted.is_(False)))
        orm_sku = result.scalars().first()

        if orm_sku is None:
            raise HTTPException(status_code=400, detail="Wrong Sku")

        sku = orm_sku.to_domain()
        return sku

    async def update_sku(self, id:int,  update_sku: SkuBase, user_id: int) -> bool:
        result = await self.db_session.execute(select(SkuOrmModel).filter(SkuOrmModel.id == id, SkuOrmModel.is_deleted.is_(False)))
        orm_sku = result.scalars().first()

        if orm_sku is None:
            raise HTTPException(status_code=400, detail="Wrong Sku")

        orm_sku = update_orm_model_from_domain(orm_sku, update_sku)
        orm_sku.updated_at = datetime.now()
        orm_sku.updated_by = user_id
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False

    async def delete_sku(self, id: int, user_id: int) -> bool:
        result = await self.db_session.execute(select(SkuOrmModel).filter(SkuOrmModel.id == id, SkuOrmModel.is_deleted.is_(False)))
        orm_sku = result.scalars().first()

        if orm_sku is None:
            raise HTTPException(status_code=400, detail="Wrong Sku")

        orm_sku.updated_at = datetime.now()
        orm_sku.is_deleted = True
        orm_sku.deleted_at = datetime.now()
        orm_sku.deleted_by = user_id
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False