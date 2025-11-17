from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from domain.models.transaction import Transaction
from infrastructure.orm.transaction_orm_model import TransactionOrmModel
from domain.repositories.transaction_repository import TransactionRepository
from typing import List, Union, Optional
import datetime
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

class SQLTransactionRepository(TransactionRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def add(self, transaction: Transaction) -> Transaction:
        transaction_result = await self.db_session.execute(
            select(TransactionOrmModel).filter(TransactionOrmModel.transaction_ref == transaction.transaction_ref)
        )
        orm_transaction = transaction_result.scalars().first()

        if orm_transaction:
            raise HTTPException(status_code=400, detail="Transaction already exists")

        orm_transaction = TransactionOrmModel.from_domain(transaction)
        self.db_session.add(orm_transaction)
        await self.db_session.commit()
        await self.db_session.refresh(orm_transaction)

        transaction_ref = f"crm-{orm_transaction.id}"
        orm_transaction.transaction_ref = transaction_ref
        self.db_session.add(orm_transaction)
        await self.db_session.commit()

        await self.db_session.refresh(orm_transaction)
        new_transaction = orm_transaction.to_domain()
        return new_transaction

    async def get_by_id(self, id: int) -> Optional[Transaction]:
        result = await self.db_session.execute(select(TransactionOrmModel).filter(TransactionOrmModel.id == id))
        orm_transaction = result.scalars().first()

        if orm_transaction:
            return orm_transaction.to_domain()
        else:
            return None

    async def get_all(self) -> List[Transaction]:
        result = await self.db_session.execute(select(TransactionOrmModel))
        orm_transactions = result.scalars().all()
        return [transaction.to_domain() for transaction in orm_transactions]

    async def update_transaction(self, id: int, user_id: int, transaction_update_dto: Transaction) -> bool:
        # Fetch the existing transaction from the database
        result = await self.db_session.execute(
            select(TransactionOrmModel).filter(TransactionOrmModel.id == id)
        )
        orm_transaction = result.scalars().first()

        if orm_transaction is None:
            return False

        if transaction_update_dto.amount is not None:
            orm_transaction.amount = transaction_update_dto.amount
        if transaction_update_dto.is_paid is not None:
            orm_transaction.is_paid = transaction_update_dto.is_paid
        if transaction_update_dto.payment_type is not None:
            orm_transaction.payment_type = transaction_update_dto.payment_type
        if transaction_update_dto.transaction_ref is not None:
            orm_transaction.transaction_ref = transaction_update_dto.transaction_ref

        orm_transaction.updated_at = datetime.datetime.now()
        orm_transaction.updated_by = user_id

        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False

    async def delete_transaction(self, id: int) -> bool:
        result = await self.db_session.execute(
            select(TransactionOrmModel).filter(TransactionOrmModel.id==id)
        )
        orm_transaction = result.scalars().first()

        if orm_transaction is None:
            return False

        await self.db_session.delete(orm_transaction)
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False