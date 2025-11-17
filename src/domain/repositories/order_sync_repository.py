from abc import ABC, abstractmethod
from typing import List
from domain.models.order import Order


class OrderSyncRepository(ABC):
    @abstractmethod
    def add_order(self, order: Order) -> Order:
        pass
