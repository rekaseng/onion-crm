from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from domain.models.order import Order


class OrdersRepository(ABC):
    @abstractmethod
    async def add(self, orders: Order, current_user: dict) -> bool:
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> List[Order]:
        pass

    @abstractmethod
    async def get_by_id(self, order_id: int) -> Order:
        pass

    @abstractmethod
    async def get_all(self, limit: int, offset: int) -> dict:
        pass

    @abstractmethod
    async def get_all_admin(self, limit: int, offset: int, start:Optional[datetime], end:Optional[datetime]) -> List[Order]:
        pass

    @abstractmethod
    async def update_orders(self, id, orders_update_dto: Order, user_id: int) -> bool:
        pass

    @abstractmethod
    async def delete_orders(self, id: int, current_user: dict) -> bool:
        pass
