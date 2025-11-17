from abc import ABC, abstractmethod
from typing import Optional, List

from domain.models.store_credits import StoreCredit


class StoreCreditRepositorySync(ABC):
    @abstractmethod
    def upsert_sync(self, store_credit: StoreCredit) -> int:
        pass