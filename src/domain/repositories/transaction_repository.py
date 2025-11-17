from abc import ABC, abstractmethod
from typing import List
from domain.models.transaction import Transaction


class TransactionRepository(ABC):
    @abstractmethod
    async def add(self, transaction: Transaction) -> Transaction:
        pass


    @abstractmethod
    async def get_by_id(self, id: int) -> Transaction:
        pass

    @abstractmethod
    async def get_all(self) -> List[Transaction]:
        pass

    @abstractmethod
    async def update_transaction(self, id: int, user_id: int, transaction_update_dto: Transaction) -> bool:
        pass

    @abstractmethod
    async def delete_transaction(self, id: int) -> bool:
        pass
