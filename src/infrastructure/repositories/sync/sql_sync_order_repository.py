from sqlalchemy.orm import Session
from domain.models.order import Order
from domain.repositories.order_sync_repository import OrderSyncRepository
from infrastructure.orm.order_orm_model import OrderOrmModel
from datetime import datetime
from sqlalchemy.future import select
from fastapi import HTTPException
from typing import List
from sqlalchemy.exc import SQLAlchemyError

class SQLSyncOrderRepository(OrderSyncRepository):

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add_order(self, order: Order) -> Order:
        orm_order = OrderOrmModel.from_domain(order)
        print(orm_order)  # Check the ORM model
        try:
            self.db_session.add(orm_order)
            self.db_session.commit()
            self.db_session.refresh(orm_order)  # Refresh to load the new ID
            new_order = orm_order.to_domain()
            return new_order
        except SQLAlchemyError as e:
            self.db_session.rollback()
            print(f"SQLAlchemyError: {str(e)}")  # Log the error
            return False


