from abc import ABC, abstractmethod
from typing import Optional, List

from domain.models.payment_method import PaymentMethod


class PaymentMethodRepository(ABC):
    @abstractmethod
    async def add(self, paymentMethod: PaymentMethod) -> bool:
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> Optional[List[PaymentMethod]]:
        pass

    @abstractmethod
    async def get_by_payment_token(self, payment_token: str) -> Optional[PaymentMethod]:
        pass

    @abstractmethod
    async def delete_payment_method(self, user_id: int) -> bool:
        pass