from abc import ABC, abstractmethod
from datetime import date
from typing import Optional, List
from domain.models.payment import Payment, PaymentBase


class PaymentRepository(ABC):
    @abstractmethod
    async def add(self, payment: Payment) -> bool:
        pass

    @abstractmethod
    async def get_by_date_range(self, start_date: date, end_date: date) -> List[Payment]:
        pass

    @abstractmethod
    async def get_by_invoice_no(self, invoice_no: str) -> Optional[Payment]:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[Payment]:
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> List[Payment]:
        pass

    @abstractmethod
    async def update_payment(self, id: int, payment_update_dto: PaymentBase) -> bool:
        pass

    @abstractmethod
    async def get_by_transaction_id(self, transaction_id: int) -> Optional[Payment]:
        pass