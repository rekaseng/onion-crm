from typing import List
from abc import ABC, abstractmethod
from domain.models.otp import Otp

class OtpRepository(ABC):
    @abstractmethod
    def add(self, otp: Otp) -> None:
        pass

    @abstractmethod
    def verify(self, full_mobile: str, otp:  str) -> bool:
        pass