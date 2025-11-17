from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy.future import select
from fastapi import HTTPException
from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError

from domain.repositories.store_credit_transaction_repository_sync import StoreCreditTransactionRepositorySync
from domain.models.store_credit_transaction import StoreCreditTransaction
from infrastructure.orm.store_credit_transaction_orm_model import StoreCreditTransactionOrmModel

class SQLSyncStoreCreditTransactionRepository(StoreCreditTransactionRepositorySync):

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add_sync(self, store_credit_transaction: StoreCreditTransaction) -> bool:

        orm_model = StoreCreditTransactionOrmModel.from_domain(store_credit_transaction)
        try:
            self.db_session.add(orm_model)
            self.db_session.commit()
            return True
        except SQLAlchemyError as e:
            self.db_session.rollback()
            print(f"SQLAlchemyError: {str(e)}")  # Log the error
            return False


