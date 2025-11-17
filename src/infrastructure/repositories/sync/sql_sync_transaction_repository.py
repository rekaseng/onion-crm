from sqlalchemy.orm import Session
from sqlalchemy.future import select
from domain.models.transaction import Transaction
from infrastructure.orm.transaction_orm_model import TransactionOrmModel
from typing import List, Union, Optional
import datetime
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from domain.repositories.transaction_repository_sync import TransactionRepositorySync

class SQLSyncTransactionRepository(TransactionRepositorySync):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add_sync(self, transaction: Transaction) -> Transaction:
        orm_transaction = self.db_session.query(TransactionOrmModel).filter(TransactionOrmModel.transaction_ref == transaction.transaction_ref).first()

        if orm_transaction:
            raise HTTPException(status_code=400, detail="Transaction already exists")

        orm_transaction = TransactionOrmModel.from_domain(transaction)
        self.db_session.add(orm_transaction)
        self.db_session.commit()
        self.db_session.refresh(orm_transaction)

        transaction_ref = f"crm-{orm_transaction.id}"
        orm_transaction.transaction_ref = transaction_ref
        self.db_session.add(orm_transaction)
        self.db_session.commit()

        self.db_session.refresh(orm_transaction)
        return orm_transaction.to_domain()
    
    def get_by_ref_sync(self, transaction_ref: str) -> Optional[Transaction]:
        orm_transaction = self.db_session.query(TransactionOrmModel).filter(TransactionOrmModel.transaction_ref == transaction_ref).first()
        return orm_transaction.to_domain() if orm_transaction else None
    
    def update_sync(self, transaction_ref: str, is_paid: bool) -> bool:
        exist_result = self.db_session.query(TransactionOrmModel).filter(TransactionOrmModel.transaction_ref == transaction_ref).first()
        try:
            if not exist_result:
                return False
            exist_result.is_paid = is_paid
            exist_result.updated_at = datetime.datetime.now()
            exist_result.updated_by = 0
            self.db_session.add(exist_result)
            self.db_session.commit()
            return True
        except SQLAlchemyError as e:
            self.db_session.rollback()
            print(f"SQLAlchemyError: {str(e)}")  # Log the error
            return False