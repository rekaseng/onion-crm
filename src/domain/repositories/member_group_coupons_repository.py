from abc import ABC, abstractmethod
from typing import List
from domain.models.member_group_coupon import MemberGroupCoupon, MemberGroupCouponBase


class MemberGroupCouponsRepository(ABC):
    @abstractmethod
    async def add(self, member_group_coupon: MemberGroupCoupon, current_user: dict) -> bool:
        pass

    @abstractmethod
    async def add_admin(self, member_group_coupon: MemberGroupCoupon) -> bool:
        pass

    @abstractmethod
    async def get_by_member_group_id(self, member_group_id: int, current_user: dict) -> List[MemberGroupCoupon]:
        pass

    @abstractmethod
    async def get_by_member_group_ids(self, member_group_ids: List[int]) -> List[MemberGroupCoupon]:
        pass

    @abstractmethod
    async def get_by_member_group_coupon_id_admin(self, member_group_coupon_id: int, current_user: dict) -> List[MemberGroupCoupon]:
        pass

    @abstractmethod
    async def get_all(self, current_user: dict) -> List[MemberGroupCoupon]:
        pass

    @abstractmethod
    async def get_all_admin(self, current_user: dict) -> List[MemberGroupCoupon]:
        pass

    @abstractmethod
    async def update_member_group_coupon(self, member_group_coupons_update_dto: MemberGroupCouponBase, current_user: dict) -> bool:
        pass

    @abstractmethod
    async def update_member_group_coupon_admin(self, member_group_coupons_update_dto: MemberGroupCouponBase, current_user: dict) -> bool:
        pass

    @abstractmethod
    async def delete_member_group_coupon(self, member_group_coupon_id: int, current_user: dict) -> bool:
        pass

    @abstractmethod
    async def delete_member_group_coupon_admin(self, member_group_coupon_id: int, current_user: dict) -> bool:
        pass
