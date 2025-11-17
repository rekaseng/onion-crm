from abc import ABC, abstractmethod

from domain.models.paynow import Paynow


class IPaymentAdapter(ABC):
    @abstractmethod
    def generate_payment_string (self, paynow: Paynow) -> str:
        pass