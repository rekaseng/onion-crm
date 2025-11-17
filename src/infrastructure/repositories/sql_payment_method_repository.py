from datetime import datetime
from typing import List, Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from infrastructure.orm.orm_update_helper import update_orm_model_from_domain
from domain.models.payment_method import PaymentMethod
from domain.repositories.payment_method_repository import PaymentMethodRepository
from infrastructure.orm.payment_method_orm_model import PaymentMethodOrmModel


class SQLPaymentMethodRepository(PaymentMethodRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def add(self, paymentMethod: PaymentMethod) -> bool:
        orm_payment_method = PaymentMethodOrmModel.from_domain(paymentMethod)
        await self.db_session.merge(orm_payment_method)
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            print(f"SQLAlchemyError occurred: {e}")  # or use logging
            return False

    async def get_by_user_id(self, user_id: int) -> Optional[List[PaymentMethod]]:
        result = await self.db_session.execute(
            select(PaymentMethodOrmModel).filter(PaymentMethodOrmModel.user_id == user_id, PaymentMethodOrmModel.is_deleted.is_(False)))
        orm_payment = result.scalars().all()
        return [item.to_domain() for item in orm_payment]
    
    async def get_by_payment_token(self, payment_token: str) -> Optional[PaymentMethod]:
        result = await self.db_session.execute(
            select(PaymentMethodOrmModel).filter(PaymentMethodOrmModel.payment_token == payment_token, PaymentMethodOrmModel.is_deleted.is_(False)))
        orm_payment = result.scalars().first()

        payment = orm_payment.to_domain() if orm_payment != None else None
        return payment
    
    async def delete_payment_method(self, user_id: int) -> bool:
        result = await self.db_session.execute(
            select(PaymentMethodOrmModel).filter(PaymentMethodOrmModel.user_id == user_id, PaymentMethodOrmModel.is_deleted.is_(False)))
        orms = result.scalars().all()
        for orm in orms:
            orm.updated_at = datetime.now()
            orm.is_deleted = True
            orm.deleted_at = datetime.now()
            orm.updated_by = user_id
            orm.deleted_by = user_id
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False