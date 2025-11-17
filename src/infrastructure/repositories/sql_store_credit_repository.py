from typing import List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from domain.models.store_credits import StoreCredit
from domain.models.store_credit_transaction import StoreCreditTransaction, StoreCreditTransactionType
from domain.repositories.store_credits_repository import StoreCreditsRepository
from infrastructure.orm.store_credits_orm_model import StoreCreditsOrmModel
from infrastructure.orm.store_credit_transaction_orm_model import StoreCreditTransactionOrmModel

from fastapi import HTTPException
from datetime import datetime
from decimal import Decimal


class SQLStoreCreditsRepository(StoreCreditsRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all(self, current_user: dict) -> List[StoreCredit]:
        result = await self.db_session.execute(
            select(StoreCreditsOrmModel).filter(StoreCreditsOrmModel.is_deleted.is_(False)))
        orm_store_credits = result.scalars().all()
        store_credits = [item.to_domain() for item in orm_store_credits]
        return store_credits
    
    async def get_by_user_id(self, user_id: int) -> List[StoreCredit]:
        result = await self.db_session.execute(
            select(StoreCreditsOrmModel).filter(StoreCreditsOrmModel.user_id == user_id, StoreCreditsOrmModel.is_deleted.is_(False)).order_by(StoreCreditsOrmModel.created_at.desc()))
        orm_store_credits = result.scalars().all()
        store_credits = [item.to_domain() for item in orm_store_credits]
        return store_credits

    async def get_all_admin(self, current_user: dict) -> List[StoreCredit]:
        result = await self.db_session.execute(
            select(StoreCreditsOrmModel).filter(StoreCreditsOrmModel.is_deleted.is_(False)))
        orm_store_credits = result.scalars().all()
        store_credits = [item.to_domain() for item in orm_store_credits]
        return store_credits

    async def add_transaction(self, admin_id: int, user_id: int, obj_in: StoreCreditTransaction) -> bool:
        query = select(StoreCreditsOrmModel).filter(
            StoreCreditsOrmModel.user_id == user_id,
            StoreCreditsOrmModel.is_deleted.is_(False)
        )
        result = await self.db_session.execute(query)
        orm_store_credit = result.scalars().first()

        if not orm_store_credit:
            raise HTTPException(status_code=400, detail="No Store Credit in DB")

        # Creating new store credits transaction entry
        new_store_credit_transaction = StoreCreditTransaction(
            created_at=datetime.now(),
            updated_at=datetime.now(),
            store_credit_id=orm_store_credit.id,
            type=obj_in.type,
            order_id=obj_in.order_id,
            user_id=obj_in.user_id,
            amount=obj_in.amount,
            is_deleted=False,
            deleted_at=None,
            created_by=admin_id,
            updated_by=admin_id,
            deleted_by=None
        )
        orm_store_credits_transaction = StoreCreditTransactionOrmModel.from_domain(
            new_store_credit_transaction)
        self.db_session.add(orm_store_credits_transaction)

        if(obj_in.type == StoreCreditTransactionType.CREDIT):
            orm_store_credit.balance = orm_store_credit.balance + Decimal(obj_in.amount)
        elif(obj_in.type == StoreCreditTransactionType.DEBIT):
            orm_store_credit.balance = orm_store_credit.balance - Decimal(obj_in.amount)

        self.db_session.add(orm_store_credit)

        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False


    async def get_store_credits_balance(self, user_id: int) -> StoreCredit:
        result = await self.db_session.execute(
            select(StoreCreditsOrmModel).filter(StoreCreditsOrmModel.user_id == user_id,
                                                StoreCreditsOrmModel.is_deleted.is_(False)))
        orm_store_credits = result.scalars().first()


        if orm_store_credits is None:
            raise HTTPException(status_code=400, detail="Wrong StoreCredits")

        store_credits = orm_store_credits.to_domain()
        return store_credits