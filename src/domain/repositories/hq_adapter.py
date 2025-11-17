from abc import ABC, abstractmethod
from typing import List

from application.dto.user_dto import MachineLoginWithUserDto
from domain.models.paynow import Paynow
from domain.models.sku import HQSku


class IHqAdapter(ABC):
    @abstractmethod
    async def machine_login (self, machine_login_dto: MachineLoginWithUserDto) -> str:
        pass

    @abstractmethod
    async def get_all_skus (self) -> List[HQSku]:
        pass