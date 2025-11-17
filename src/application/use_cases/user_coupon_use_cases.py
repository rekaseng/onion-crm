from typing import List, Optional

from domain.models.coupon import Coupon, CouponBase
from domain.models.coupon_definition import CouponDefinition
from domain.models.full_coupon import FullCoupon
from domain.repositories.coupon_definition_repository import CouponDefinitionRepository
from domain.repositories.coupon_repository import CouponRepository
from datetime import datetime

from domain.repositories.user_coupon_repository import UserCouponRepository
from domain.models.user_coupon import UserCoupon, UserCouponBase
from domain.repositories.member_groups_repository import MemberGroupsRepository
from domain.repositories.member_group_coupons_repository import MemberGroupCouponsRepository
from domain.repositories.user_coupon_usage_repository import UserCouponUsageRepository


class UserCouponUseCases:
    def __init__(self, user_coupon_repository: UserCouponRepository, coupon_definition_repository: CouponDefinitionRepository, member_group_repository: Optional[MemberGroupsRepository] = None, member_group_coupon_repository: Optional[MemberGroupCouponsRepository] = None, user_coupon_usage_repository: Optional[UserCouponUsageRepository] = None):
        self.user_coupon_repository = user_coupon_repository
        self.coupon_definition_repository = coupon_definition_repository
        self.member_group_repository = member_group_repository
        self.member_group_coupon_repository = member_group_coupon_repository
        self.user_coupon_usage_repository = user_coupon_usage_repository

    async def get_coupons_by_user_id(self, user_id: int) -> List[CouponDefinition]:
        coupon_definitions = await self.coupon_definition_repository.get_all()
        return coupon_definitions

    async def get_full_coupons_by_user_id(self, user_id: int) -> List[FullCoupon]:
        #find coupons:
        #a) if the coupon is assigned to this user through user_coupon or member_group_coupon
        #b) if this user usage has not reached its redemption limit

        coupon_definitions = await self.coupon_definition_repository.get_all()
        coupon_definition_dict = {}
        for definition in coupon_definitions:
                coupon_definition_dict[definition.id] = definition

        member_groups = await self.member_group_repository.get_by_user_id(user_id)
        member_group_ids = [item.id for item in member_groups]

        user_coupon_usages = await self.user_coupon_usage_repository.get_by_user_id(user_id)
        user_coupon_usage_dict = {}
        member_group_coupon_usage_dict = {}
        for usage in user_coupon_usages:
            if usage.user_coupon_id:
                if usage.user_coupon_id not in user_coupon_usage_dict:
                    user_coupon_usage_dict[usage.user_coupon_id] = 0
                user_coupon_usage_dict[usage.user_coupon_id] += 1

            if usage.member_group_coupon_id:
                    usage_key = f'{usage.member_group_coupon_id}'
                    if usage.member_group_coupon_id not in member_group_coupon_usage_dict:
                        member_group_coupon_usage_dict[usage_key] = 0
                    member_group_coupon_usage_dict[usage_key] += 1


        user_coupons = await self.user_coupon_repository.get_user_coupon_by_user_id(user_id)
        member_group_coupons = await self.member_group_coupon_repository.get_by_member_group_ids(member_group_ids)
            
        full_coupons = []
        for user_coupon in user_coupons:
            redemption_count = user_coupon_usage_dict[user_coupon.id] if user_coupon.id in user_coupon_usage_dict else 0
            # if user_coupon.user_redemption_period_limit <= redemption_count:
            if 1 <= redemption_count:
                continue
            coupon_definition = coupon_definition_dict[user_coupon.coupon_definition_id] if user_coupon.coupon_definition_id in coupon_definition_dict else None
            if coupon_definition == None:
                continue

            full_coupon = FullCoupon(
                id = coupon_definition.id,
                name = user_coupon.name,
                code = coupon_definition.code,
                discount_type = coupon_definition.discount_type,
                discount_amount = coupon_definition.discount_amount,
                minimum_spending = coupon_definition.minimum_spending,
                minimum_spending_active = coupon_definition.minimum_spending_active,
                criterial_cart_type = coupon_definition.criterial_cart_type,
                criterial_cart_skus = coupon_definition.criterial_cart_skus,
                criterial_cart_collections = coupon_definition.criterial_cart_collections,
                active = coupon_definition.active,
                target_type = coupon_definition.target_type,
                target_skus = coupon_definition.target_skus,
                target_collections = coupon_definition.target_collections,
                is_deleted = False,
                is_global = coupon_definition.is_global,
                member_group_coupon_id = None,
                user_coupon_id = user_coupon.id,
                date_start = user_coupon.date_start,
                date_end = user_coupon.date_end,
                all_machines = user_coupon.all_machines,
                applicable_machines = user_coupon.applicable_machines,
                user_redemption_period_limit = user_coupon.user_redemption_period_limit,
                user_redemption_period_type = user_coupon.user_redemption_period_type,
            )
            full_coupons.append(full_coupon)


        for member_group_coupon in member_group_coupons:
            # assume no limit first
            # redemption_count = member_group_coupon_usage_dict[member_group_coupon.id] if member_group_coupon.id in member_group_coupon_usage_dict else 0
            # if member_group_coupon.group_redemption_period_limit <= redemption_count:
            #     continue

            usage_key = f'{member_group_coupon.id}'
            redemption_count = member_group_coupon_usage_dict[usage_key] if usage_key in member_group_coupon_usage_dict else 0
            if member_group_coupon.user_redemption_period_limit <= redemption_count:
                continue

            coupon_definition = coupon_definition_dict[member_group_coupon.coupon_definition_id] if member_group_coupon.coupon_definition_id in coupon_definition_dict else None
            if coupon_definition == None:
                continue

            full_coupon = FullCoupon(
                id = coupon_definition.id,
                name = member_group_coupon.name,
                code = coupon_definition.code,
                discount_type = coupon_definition.discount_type,
                discount_amount = coupon_definition.discount_amount,
                minimum_spending = coupon_definition.minimum_spending,
                minimum_spending_active = coupon_definition.minimum_spending_active,
                criterial_cart_type = coupon_definition.criterial_cart_type,
                criterial_cart_skus = coupon_definition.criterial_cart_skus,
                criterial_cart_collections = coupon_definition.criterial_cart_collections,
                active = coupon_definition.active,
                target_type = coupon_definition.target_type,
                target_skus = coupon_definition.target_skus,
                target_collections = coupon_definition.target_collections,
                is_deleted = False,
                is_global = coupon_definition.is_global,
                member_group_coupon_id = member_group_coupon.id,
                user_coupon_id = None,
                date_start = member_group_coupon.date_start,
                date_end = member_group_coupon.date_end,
                all_machines = member_group_coupon.all_machines,
                applicable_machines = member_group_coupon.applicable_machines,
                user_redemption_period_limit = member_group_coupon.group_redemption_period_limit,
                user_redemption_period_type = member_group_coupon.group_redemption_period_type,
            )
            full_coupons.append(full_coupon)


        return full_coupons
    
    async def add(self, coupon_dto: UserCouponBase, user_id: int) -> bool:
        coupon = UserCoupon(
            created_at=datetime.now(),
            updated_at=datetime.now(),
            is_deleted=False,
            user_id = coupon_dto.user_id,
            coupon_definition_id=coupon_dto.coupon_definition_id,
            name = coupon_dto.name,
            date_start = coupon_dto.date_start,
            date_end = coupon_dto.date_end,
            all_machines = coupon_dto.all_machines,
            applicable_machines = coupon_dto.applicable_machines,
            user_redemption_period_limit = coupon_dto.user_redemption_period_limit,
            user_redemption_period_type = coupon_dto.user_redemption_period_type,
            created_by=user_id,
            updated_by=user_id,
            deleted_at=None,
            deleted_by=None
        )
        coupon = await self.user_coupon_repository.add(coupon)
        return coupon
    
    async def get_all(self) -> List[UserCoupon]:
        coupons = await self.user_coupon_repository.get_all()
        return coupons
    
    async def get_by_id(self, id: int) -> UserCoupon:
        coupon = await self.user_coupon_repository.get_by_id(id)
        return coupon
    
    async def update_user_coupon(self, id: int, coupon_update_dto: UserCouponBase, user_id: int) -> bool:
        coupon = await self.user_coupon_repository.update_user_coupon(id, coupon_update_dto, user_id)
        return coupon
    
    async def delete_user_coupon(self, id: int, user_id: int) -> bool:
        coupon = await self.user_coupon_repository.delete_user_coupon(id, user_id)
        return coupon


