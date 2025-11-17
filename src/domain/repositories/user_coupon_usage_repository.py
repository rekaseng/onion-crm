from abc import ABC, abstractmethod
from typing import List
from domain.models.user_coupon_usage import UserCouponUsage


class UserCouponUsageRepository(ABC):
    @abstractmethod
    def add(self, user_coupon_usage: UserCouponUsage) -> bool:
        pass

    @abstractmethod
    async def get_all(self) -> List[UserCouponUsage]:
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> List[UserCouponUsage]:
        pass
