from abc import ABC, abstractmethod
from typing import Optional, List
from domain.models.coupon import Coupon, CouponBase


class CouponRepository(ABC):
    @abstractmethod
    async def add(self, coupon: Coupon) -> bool:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[Coupon]:
        pass

    @abstractmethod
    async def get_by_ids(self, ids: List[int]) -> List[Coupon]:
        pass

    @abstractmethod
    async def get_by_id_admin(self, id: int,  tenant_id: int) -> Optional[Coupon]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Coupon]:
        pass

    @abstractmethod
    async def get_all_admin(self, tenant_id: int) -> List[Coupon]:
        pass

    @abstractmethod
    async def update_coupon(self, id: int, coupon_update_dto: CouponBase, user_id: int) -> bool:
        pass

    @abstractmethod
    async def update_coupon_admin(self, id: int, coupon_update_dto: CouponBase, user_id: int, tenant_id: int) -> bool:
        pass

    @abstractmethod
    async def delete_coupon(self, id: int, user_id: int) -> bool:
        pass

    @abstractmethod
    async def delete_coupon_admin(self, id: int, user_id: int, tenant_id: int) -> bool:
        pass