from abc import ABC, abstractmethod
from typing import List, Optional
from domain.models.transaction import Transaction


class TransactionRepositorySync(ABC):
    @abstractmethod
    def add_sync(self, transaction: Transaction) -> bool:
        pass

    @abstractmethod
    def get_by_ref_sync(self, transaction_ref: str) -> Optional[Transaction]:
        pass
