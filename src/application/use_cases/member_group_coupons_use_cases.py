from typing import List

from domain.models.member_group_coupon import MemberGroupCoupon, MemberGroupCouponBase
from domain.repositories.member_group_coupons_repository import MemberGroupCouponsRepository
from datetime import datetime


class MemberGroupCouponsUseCases:
    def __init__(self, member_group_coupons_repository: MemberGroupCouponsRepository):
        self.member_group_coupons_repository = member_group_coupons_repository

    async def add(self, member_group_coupons_dto: MemberGroupCouponBase, current_user: dict) -> MemberGroupCoupon:
        member_group_coupon = MemberGroupCoupon(
            created_at=datetime.now(),
            updated_at=datetime.now(),
            member_group_id=member_group_coupons_dto.member_group_id,
            coupon_definition_id=member_group_coupons_dto.coupon_definition_id,
            is_deleted=False,
            deleted_at=None,
            created_by=current_user["user"].id,
            updated_by=current_user["user"].id,
            deleted_by=None
        )
        await self.member_group_coupons_repository.add(member_group_coupon, current_user)
        return member_group_coupon

    async def add_admin(self, member_group_coupons_dto: MemberGroupCouponBase, user_id: int) -> MemberGroupCoupon:
        obj_in = member_group_coupons_dto
        member_group_coupon = MemberGroupCoupon(
            created_at=datetime.now(),
            updated_at=datetime.now(),
            member_group_id=obj_in.member_group_id,
            coupon_definition_id=obj_in.coupon_definition_id,
            name = obj_in.name,
            date_start= obj_in.date_start,
            date_end= obj_in.date_end,
            all_machines = obj_in.all_machines,
            applicable_machines= obj_in.applicable_machines,

            user_redemption_period_limit= obj_in.user_redemption_period_limit,
            user_redemption_period_type= obj_in.user_redemption_period_type,
            group_redemption_period_limit= obj_in.group_redemption_period_limit,
            group_redemption_period_type= obj_in.group_redemption_period_type,

            is_deleted=False,
            deleted_at=None,
            created_by= user_id,
            updated_by= user_id,
            deleted_by=None
        )
        await self.member_group_coupons_repository.add_admin(member_group_coupon)
        return member_group_coupon

    async def get_all(self, current_user: dict) -> List[MemberGroupCoupon]:
        member_group_coupons = await self.member_group_coupons_repository.get_all(current_user)
        return member_group_coupons

    async def get_all_admin(self, current_user: dict) -> List[MemberGroupCoupon]:
        member_group_coupons = await self.member_group_coupons_repository.get_all_admin(current_user)
        return member_group_coupons

    async def get_by_member_group_id(self, member_group_id: int, current_user: dict) -> List[MemberGroupCoupon]:
        member_group_coupons = await self.member_group_coupons_repository.get_by_member_group_id(member_group_id,
                                                                                                 current_user)
        return member_group_coupons

    async def get_by_member_group_coupon_id_admin(self, member_group_coupon_id: int, current_user: dict) -> List[MemberGroupCoupon]:
        member_group_coupons = await self.member_group_coupons_repository.get_by_member_group_coupon_id_admin(
            member_group_coupon_id,
            current_user)
        return member_group_coupons

    async def update_member_group_coupons(self, member_group_coupons_update_dto: MemberGroupCouponBase,
                                          current_user: dict) -> bool:
        member_group_coupon = await self.member_group_coupons_repository.update_member_group_coupon(
            member_group_coupons_update_dto,
            current_user)
        return member_group_coupon

    async def update_member_group_coupons_admin(self, member_group_coupons_update_dto: MemberGroupCouponBase,
                                                current_user: dict) -> bool:
        member_group_coupon = await self.member_group_coupons_repository.update_member_group_coupon_admin(
            member_group_coupons_update_dto,
            current_user)
        return member_group_coupon

    async def delete_member_group_coupons(self, member_group_coupon_id: int, current_user: dict) -> bool:
        member_group_coupon = await self.member_group_coupons_repository.delete_member_group_coupon(member_group_coupon_id,
                                                                                                    current_user)
        return member_group_coupon

    async def delete_member_group_coupons_admin(self, member_group_coupon_id: int, current_user: dict) -> bool:
        member_group_coupon = await self.member_group_coupons_repository.delete_member_group_coupon_admin(
            member_group_coupon_id,
            current_user)
        return member_group_coupon
