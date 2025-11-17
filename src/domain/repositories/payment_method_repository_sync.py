from abc import ABC, abstractmethod
from typing import Optional, List

from domain.models.payment_method import PaymentMethod


class PaymentMethodRepositorySync(ABC):
    @abstractmethod
    def get_by_user_id_sync(self, user_id: int) -> Optional[List[PaymentMethod]]:
        pass