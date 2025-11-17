from abc import ABC, abstractmethod
from typing import Optional, List
from domain.models.payment import Payment, PaymentBase


class PaymentRepositorySync(ABC):
    @abstractmethod
    def add_sync(self, payment: Payment) -> bool:
        pass