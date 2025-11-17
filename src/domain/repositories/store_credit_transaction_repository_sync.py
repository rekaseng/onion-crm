from abc import ABC, abstractmethod
from typing import Optional, List

from domain.models.store_credit_transaction import StoreCreditTransaction


class StoreCreditTransactionRepositorySync(ABC):
    @abstractmethod
    def add_sync(self, store_credit_transaction: StoreCreditTransaction) -> bool:
        pass