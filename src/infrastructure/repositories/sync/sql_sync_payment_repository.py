from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy.future import select
from fastapi import HTTPException
from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError
from domain.repositories.payment_repository import PaymentRepository
from domain.models.payment import Payment
from infrastructure.orm.payment_orm_model import PaymentOrmModel
from domain.repositories.payment_repository_sync import PaymentRepositorySync

class SQLSyncPaymentRepository(PaymentRepositorySync):

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add_sync(self, payment: Payment) -> bool:
        payment_result = self.db_session.query(PaymentOrmModel).filter(PaymentOrmModel.invoice_no == payment.invoice_no).filter(PaymentOrmModel.is_deleted == False).first()

        if payment_result:
            raise HTTPException(status_code=400, detail="Payment with this invoice no already exists")

        orm_payment = PaymentOrmModel.from_domain(payment)
        try:
            self.db_session.add(orm_payment)
            self.db_session.commit()
            return True
        except SQLAlchemyError as e:
            self.db_session.rollback()
            print(f"SQLAlchemyError: {str(e)}")  # Log the error
            return False


