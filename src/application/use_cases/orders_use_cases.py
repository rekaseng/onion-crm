from typing import List

from domain.models.order import Order, OrderBase
from domain.repositories.order_repository import OrdersRepository
from domain.repositories.sku_repository import SkuRepository
from datetime import datetime


class OrdersUseCases:
    def __init__(self, orders_repository: OrdersRepository, sku_repository: SkuRepository):
        self.orders_repository = orders_repository
        self.sku_repository = sku_repository

    async def add(self, orders_dto: Order, user_id: int, tenant_id: int) -> bool:
        orders = Order(
            created_at=datetime.now(),
            updated_at=datetime.now(),
            user_id=user_id,
            tenant_id=tenant_id,
            machine_contract_id=None,
            subtotal=orders_dto.subtotal,
            payment_amount=orders_dto.payment_amount,
            items=orders_dto.items,
            payments=orders_dto.payments,
            is_deleted=False,
            deleted_at=None,
            created_by=user_id,
            updated_by=user_id,
            deleted_by=None
        )
        await self.orders_repository.add(orders)
        return orders

    async def get_all(self, limit: int, offset: int) -> dict:
        orders = await self.orders_repository.get_all(limit, offset)
        return orders

    async def get_by_id(self, id: int) -> Order:
        order = await self.orders_repository.get_by_id(id)
        skus = await self.sku_repository.get_all()
        
        # Create mapping of source_id to SKU details
        sku_dict = {sku.source_id: sku for sku in skus}
        
        # Update order items with SKU details
        for item in order.items:
            item.sku_sku = None
            item.sku_name = None
            
            if item.sku_id in sku_dict:
                sku = sku_dict[item.sku_id]
                item.sku_sku = sku.sku
                item.sku_name = sku.name
            else:
                print(f"Warning: No SKU found for sku_id {item.sku_id}")
        
        return order

    async def get_all_admin(self, limit: int, offset: int, start_datetime:datetime, end_datetime:datetime) -> dict:
        orders = await self.orders_repository.get_all_admin(limit, offset, start_datetime, end_datetime)
        return orders

    async def get_by_user_id(self, user_id: int) -> List[Order]:
        orders = await self.orders_repository.get_by_user_id(user_id)
        skus = await self.sku_repository.get_all()
        
        # Mapping source_id to SKU details
        sku_dict = {sku.source_id: sku for sku in skus}
        
        # Update each order's items with SKU details
        for order in orders:
            for item in order.items:
                item.sku_sku = None
                item.sku_name = None
                
                if item.sku_id in sku_dict:
                    sku = sku_dict[item.sku_id]
                    item.sku_sku = sku.sku
                    item.sku_name = sku.name
                else:
                    print(f"No SKU found for sku_id {item.sku_id}")
        
        return orders

    async def update_orders(self, id, orders_update_dto: Order, user_id: int) -> bool:
        order = await self.orders_repository.update_orders(id, orders_update_dto, user_id )
        return order

    async def delete_orders(self, id: int, user_id: int) -> bool:
        order = await self.orders_repository.delete_orders(id, user_id)
        return order


