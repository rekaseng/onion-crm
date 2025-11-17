from typing import List, Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from domain.models.payment import Payment, PaymentBase
from domain.repositories.payment_repository import PaymentRepository
from infrastructure.orm.payment_orm_model import PaymentOrmModel
from fastapi import HTTPException
from datetime import date, datetime

from infrastructure.orm.orm_update_helper import update_orm_model_from_domain


class SQLPaymentRepository(PaymentRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def add(self, payment: Payment) -> bool:
        payment_result = await self.db_session.execute(select(PaymentOrmModel).filter_by(invoice_no=payment.invoice_no))
        orm_payment = payment_result.scalars().first()

        if orm_payment:
            raise HTTPException(status_code=400, detail="Payment with this invoice no already exists")

        orm_payment = PaymentOrmModel.from_domain(payment)
        await self.db_session.merge(orm_payment)
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False

    async def get_by_invoice_no(self, invoice_no: str) -> Payment:
        result = await self.db_session.execute(
            select(PaymentOrmModel).filter(PaymentOrmModel.invoice_no == invoice_no, PaymentOrmModel.is_deleted.is_(False)))
        orm_payment = result.scalars().first()

        if orm_payment is None:
            raise HTTPException(status_code=400, detail="Wrong Payment")

        payment = orm_payment.to_domain()
        return payment
    
    async def get_by_id(self, id: int) -> Optional[Payment]:
        result = await self.db_session.execute(
            select(PaymentOrmModel).filter(PaymentOrmModel.id == id, PaymentOrmModel.is_deleted.is_(False)))
        orm_payment = result.scalars().first()

        if orm_payment is None:
            raise HTTPException(status_code=400, detail="Wrong Payment")

        payment = orm_payment.to_domain()
        return payment

    async def update_payment(self, id: int, update_payment: PaymentBase) -> bool:
        payment_result = await self.db_session.execute(
            select(PaymentOrmModel).filter(PaymentOrmModel.id == id,
                                          PaymentOrmModel.is_deleted.is_(False)))
        orm_payment = payment_result.scalars().first()

        if orm_payment is None:
            raise HTTPException(status_code=400, detail="Wrong Payment")
        orm_payment = update_orm_model_from_domain(orm_payment, update_payment)
        orm_payment.updated_at = datetime.now()
        orm_payment.deleted_by = None
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False
        
    async def get_by_date_range(self, start_date: date, end_date: date) -> List[Payment]:
        result = await self.db_session.execute(
            select(PaymentOrmModel).filter(PaymentOrmModel.created_at >=  datetime.combine(start_date, datetime.min.time()), PaymentOrmModel.created_at <=  datetime.combine(end_date, datetime.max.time()), PaymentOrmModel.is_deleted.is_(False)))
        orm_payment = result.scalars().all()
        return [item.to_domain() for item in orm_payment]
    
    async def get_by_user_id(self, user_id: int) -> List[Payment]:
        result = await self.db_session.execute(
            select(PaymentOrmModel).filter(PaymentOrmModel.user_id == user_id, PaymentOrmModel.is_deleted.is_(False)))
        orm_payment = result.scalars().all()
        return [item.to_domain() for item in orm_payment]

    async def get_by_transaction_id(self, transaction_id: int) -> Optional[Payment]:
        result = await self.db_session.execute(
            select(PaymentOrmModel).filter(
                PaymentOrmModel.transaction_id == transaction_id,
                PaymentOrmModel.is_deleted.is_(False)
            )
        )
        orm_payment = result.scalars().first()
        
        if orm_payment is None:
            return None
            
        return orm_payment.to_domain()