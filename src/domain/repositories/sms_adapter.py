from abc import ABC, abstractmethod

from domain.models.paynow import Paynow
from domain.models.sms_message import SmsMessage


class ISmsAdapter(ABC):
    @abstractmethod
    def send_sms(self, message: SmsMessage) -> bool:
        pass