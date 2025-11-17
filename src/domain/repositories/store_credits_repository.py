from abc import ABC, abstractmethod
from typing import Union, List
from domain.models.store_credit_transaction import StoreCreditTransaction
from domain.models.store_credits import StoreCredit

class StoreCreditsRepository(ABC):
    @abstractmethod
    async def add_transaction(self, admin_id: int, user_id:int, store_credits_transaction: StoreCreditTransaction) -> bool:
        pass

    @abstractmethod
    async def get_store_credits_balance(self, user_id: int) -> Union[StoreCredit, None]:
        pass

    @abstractmethod
    async def get_all(self, current_user: dict) -> List[StoreCredit]:
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> List[StoreCredit]:
        pass
