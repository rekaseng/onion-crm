from abc import ABC, abstractmethod
from typing import Optional, List
from domain.models.coupon import Coupon
from domain.models.user_coupon import UserCoupon, UserCouponBase


class UserCouponRepository(ABC):
    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> Optional[Coupon]:
        pass

    @abstractmethod
    async def add(self, coupon: UserCoupon) -> bool:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[UserCoupon]:
        pass

    @abstractmethod
    async def get_by_ids(self, ids: List[int]) -> List[UserCoupon]:
        pass

    @abstractmethod
    async def get_all(self) -> List[UserCoupon]:
        pass

    @abstractmethod
    async def update_user_coupon(self, id: int, coupon_update_dto: UserCouponBase, user_id: int) -> bool:
        pass

    @abstractmethod
    async def delete_user_coupon(self, id: int, user_id: int) -> bool:
        pass

    @abstractmethod
    async def get_user_coupon_by_user_id(self, user_id: int) -> List[UserCoupon]:
        pass

