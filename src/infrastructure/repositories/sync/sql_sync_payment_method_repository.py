from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy.future import select
from fastapi import HTTPException
from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError
from domain.repositories.payment_method_repository import PaymentMethodRepository
from domain.models.payment_method import PaymentMethod
from infrastructure.orm.payment_method_orm_model import PaymentMethodOrmModel
from domain.repositories.payment_method_repository_sync import PaymentMethodRepositorySync

class SQLSyncPaymentMethodRepository(PaymentMethodRepositorySync):

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_by_user_id_sync(self, user_id: int) -> Optional[List[PaymentMethod]]:
        return self.db_session.query(PaymentMethodOrmModel).filter(PaymentMethodOrmModel.user_id == user_id).filter(PaymentMethodOrmModel.is_deleted == False).all()


