from decimal import Decimal
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy.future import select
from fastapi import HTTPException
from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError

from domain.repositories.store_credit_repository_sync import StoreCreditRepositorySync
from domain.models.store_credits import StoreCredit
from infrastructure.orm.store_credits_orm_model import StoreCreditsOrmModel
from domain.models.store_credit_transaction import StoreCreditTransactionType

class SQLSyncStoreCreditRepository(StoreCreditRepositorySync):

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def upsert_sync(self, store_credit: StoreCredit) -> int:
        exist_result = self.db_session.query(StoreCreditsOrmModel).filter(StoreCreditsOrmModel.user_id == store_credit.user_id).filter(StoreCreditsOrmModel.is_deleted == False).first()
        try:
            if exist_result:
                if store_credit.type == StoreCreditTransactionType.DEBIT:
                    exist_result.balance = exist_result.balance - Decimal(store_credit.latest_amount)
                elif store_credit.type == StoreCreditTransactionType.CREDIT:
                    exist_result.balance = exist_result.balance + Decimal(store_credit.latest_amount)
                exist_result.updated_at = datetime.now()
                self.db_session.add(exist_result)
                self.db_session.commit()
                return exist_result.id
            else:
                orm_store_credit = StoreCreditsOrmModel.from_domain(store_credit)
                self.db_session.add(orm_store_credit)
                self.db_session.commit()
                self.db_session.refresh(orm_store_credit)
                return orm_store_credit.id
        except SQLAlchemyError as e:
            self.db_session.rollback()
            print(f"SQLAlchemyError: {str(e)}")  # Log the error
            return False


