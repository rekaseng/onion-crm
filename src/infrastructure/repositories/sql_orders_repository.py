from typing import List, Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, desc
from domain.models.order import Order, OrderBase
from domain.repositories.order_repository import OrdersRepository
from infrastructure.orm.order_orm_model import OrderOrmModel
from fastapi import HTTPException
from datetime import datetime

from infrastructure.orm.orm_update_helper import update_orm_model_from_domain
from infrastructure.orm.sku_orm_model import SkuOrmModel


class SQLOrdersRepository(OrdersRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all(self, limit: int, offset: int) -> dict:
        total_result = await self.db_session.execute(
            select(func.count(OrderOrmModel.id)).filter(OrderOrmModel.is_deleted.is_(False))
        )
        total = total_result.scalar()

        result = await self.db_session.execute(
            select(OrderOrmModel)
            .filter(OrderOrmModel.is_deleted.is_(False))
            .limit(limit)
            .offset(offset)
        )
        orm_orders = result.scalars().all()
        orders = [item.to_domain() for item in orm_orders]
        return {"total": total, "limit": limit, "offset": offset, "orders": orders}

    async def get_all_admin(self, limit: int, offset: int, start:Optional[datetime], end:Optional[datetime]) -> dict:
        query = select(OrderOrmModel).filter(
            OrderOrmModel.is_deleted.is_(False)
        )
        if start:
            query = query.filter(OrderOrmModel.created_at >= start)
        if end:
            query = query.filter(OrderOrmModel.created_at <= end)

        # Get the total count
        total_result = await self.db_session.execute(
            query.with_only_columns(func.count(OrderOrmModel.id))
        )
        total = total_result.scalar()

        result = await self.db_session.execute(
            query.limit(limit).offset(offset).order_by(OrderOrmModel.created_at.desc())
        )
        orm_orders = result.scalars().all()
        orders = [item.to_domain() for item in orm_orders]

        return {"total": total, "limit": limit, "offset": offset, "orders": orders}

    async def add(self, orders: Order) -> bool:
        orders_result = await self.db_session.execute(select(OrderOrmModel).filter_by(id=orders.id))
        orm_orders = orders_result.scalars().first()

        if orm_orders:
            raise HTTPException(status_code=400, detail="Orders with this code already exists")

        orm_orders = OrderOrmModel.from_domain(orders)
        await self.db_session.merge(orm_orders)
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False

    async def get_by_id(self, order_id: int) -> Order:
        result = await self.db_session.execute(
            select(OrderOrmModel).filter(
                OrderOrmModel.id == order_id,
                OrderOrmModel.is_deleted.is_(False)
            )
        )
        orm_order = result.scalars().first()
        if orm_order is None:
            raise HTTPException(status_code=400, detail="Orders with this id not found")
        return orm_order.to_domain()

    async def get_by_user_id(self, user_id: int) -> List[Order]:
        query = select(OrderOrmModel).filter(OrderOrmModel.user_id == user_id,
                                         OrderOrmModel.is_deleted.is_(False))
        query = query.order_by(desc(OrderOrmModel.id))
        result = await self.db_session.execute(query)
        orm_orders = result.scalars().all()

        if orm_orders is None:
            raise HTTPException(status_code=400, detail="Wrong User Order")

        skus = (await self.db_session.execute(select(SkuOrmModel))).scalars().all()
        sku_dict = {}
        for sku in skus:
            sku_dict[sku.sku] = sku.to_domain()

        orders = [item.to_domain(sku_dict) for item in orm_orders]
        return orders

    async def update_orders(self, id:int, update_orders: Order, user_id: int) -> bool:
        orders_result = await self.db_session.execute(
            select(OrderOrmModel).filter(OrderOrmModel.id == id,
                                         OrderOrmModel.is_deleted.is_(False)))
        orm_orders = orders_result.scalars().first()

        if orm_orders is None:
            raise HTTPException(status_code=400, detail="Wrong Orders")

        orm_orders = update_orm_model_from_domain(orm_orders, update_orders)
        orm_orders.updated_at = datetime.now()
        orm_orders.created_by = user_id
        orm_orders.updated_by = user_id
        orm_orders.deleted_by = None
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False

    async def delete_orders(self, id: int, user_id: int) -> bool:
        orders_result = await self.db_session.execute(select(OrderOrmModel).filter(OrderOrmModel.id == id,
                                                                                   OrderOrmModel.is_deleted.is_(
                                                                                        False)))
        orm_orders = orders_result.scalars().first()

        if orm_orders is None:
            raise HTTPException(status_code=400, detail="Wrong Orders")

        orm_orders.updated_at = datetime.now()
        orm_orders.is_deleted = True
        orm_orders.deleted_at = datetime.now()
        orm_orders.updated_by = user_id
        orm_orders.deleted_by = user_id
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False
