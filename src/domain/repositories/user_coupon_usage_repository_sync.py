from abc import ABC, abstractmethod
from typing import Optional, List

from domain.models.user_coupon_usage import UserCouponUsage


class UserCouponUsageRepositorySync(ABC):
    @abstractmethod
    def add_sync(self, user_coupon_usage: UserCouponUsage) -> bool:
        pass