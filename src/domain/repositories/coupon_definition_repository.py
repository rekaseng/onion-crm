from abc import ABC, abstractmethod
from typing import Optional, List

from domain.models.coupon_definition import CouponDefinition, CouponDefinitionBase


class CouponDefinitionRepository(ABC):
    @abstractmethod
    async def add(self, coupon: CouponDefinition) -> bool:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[CouponDefinition]:
        pass

    @abstractmethod
    async def get_by_ids(self, ids: List[int]) -> List[CouponDefinition]:
        pass

    @abstractmethod
    async def get_by_id_admin(self, id: int,  tenant_id: int) -> Optional[CouponDefinition]:
        pass

    @abstractmethod
    async def get_all(self) -> List[CouponDefinition]:
        pass

    @abstractmethod
    async def get_all_admin(self, tenant_id: int) -> List[CouponDefinition]:
        pass

    @abstractmethod
    async def update_coupon_definition(self, id: int, coupon_update_dto: CouponDefinitionBase, user_id: int) -> bool:
        pass

    @abstractmethod
    async def update_coupon_definition_admin(self, id: int, coupon_update_dto: CouponDefinitionBase, user_id: int, tenant_id: int) -> bool:
        pass

    @abstractmethod
    async def delete_coupon_definition(self, id: int, user_id: int) -> bool:
        pass

    @abstractmethod
    async def delete_coupon_definition_admin(self, id: int, user_id: int, tenant_id: int) -> bool:
        pass