from typing import List
from domain.models.order import Order, OrderBase
from datetime import datetime

from domain.repositories.order_sync_repository import OrderSyncRepository


class SyncOrdersUseCases:
    def __init__(self, orders_repository: OrderSyncRepository):
        self.orders_repository = orders_repository

    def add_order(self, order_dto: Order) -> Order:
        order = Order(
            created_at=datetime.now(),
            updated_at=datetime.now(),
            user_id=order_dto.user_id,
            order_ref=order_dto.order_ref,
            machine_id=order_dto.machine_id,
            tenant_id=1, #todo:syd check tenant
            machine_contract_id=None,
            subtotal=order_dto.subtotal,
            payment_amount=order_dto.payment_amount,
            items=order_dto.items,
            payments=order_dto.payments,
            is_deleted=False,
            deleted_at=None,
            created_by=None,
            updated_by=None,
            deleted_by=None
        )
        return self.orders_repository.add_order(order)