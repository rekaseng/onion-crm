from typing import List

from domain.models.coupon import Coupon, CouponBase
from domain.repositories.coupon_repository import CouponRepository
from datetime import datetime

class CouponUseCases:
    def __init__(self, coupon_repository: CouponRepository):
        self.coupon_repository = coupon_repository

    async def add(self, coupon_dto: CouponBase, user_id: int, tenant_id: int) -> bool:
        coupon = Coupon(
            created_at=datetime.now(),
            updated_at=datetime.now(),
            name=coupon_dto.name,
            code=coupon_dto.code,
            discount_type=coupon_dto.discount_type,
            discount_amount=coupon_dto.discount_amount,
            minimum_spending=coupon_dto.minimum_spending,
            minimum_spending_active=coupon_dto.minimum_spending_active,
            criterial_cart_type=coupon_dto.criterial_cart_type,
            criterial_cart_skus=coupon_dto.criterial_cart_skus,
            criterial_cart_collections=coupon_dto.criterial_cart_collections,
            active=coupon_dto.active,
            target_type=coupon_dto.target_type,
            target_skus=coupon_dto.target_skus,
            target_collections=coupon_dto.target_collections,
            tenant_id=tenant_id,
            is_global=False,
            is_deleted=False,
            deleted_at=None,
            created_by=user_id,
            updated_by=user_id,
            deleted_by=None
        )
        coupon = await self.coupon_repository.add(coupon)
        return coupon

    async def get_all(self) -> List[Coupon]:
        coupons = await self.coupon_repository.get_all()
        return coupons

    async def get_all_admin(self, tenant_id: int) -> List[Coupon]:
        coupons = await self.coupon_repository.get_all_admin(tenant_id)
        return coupons

    async def get_by_id(self, id: int) -> Coupon:
        coupon = await self.coupon_repository.get_by_id(id)
        return coupon

    async def get_by_id_admin(self, id: int, tenant_id: int) -> Coupon:
        coupon = await self.coupon_repository.get_by_id_admin(id, tenant_id)
        return coupon

    async def update_coupon(self, id: int, coupon_update_dto: CouponBase, user_id: int) -> bool:
        coupon = await self.coupon_repository.update_coupon(id, coupon_update_dto, user_id)
        return coupon

    async def update_coupon_admin(self, id: int, coupon_update_dto: CouponBase, user_id: int, tenant_id: int) -> bool:
        coupon = await self.coupon_repository.update_coupon_admin(id, coupon_update_dto, user_id, tenant_id)
        return coupon

    async def delete_coupon(self, id: int, user_id: int) -> bool:
        coupon = await self.coupon_repository.delete_coupon(id, user_id)
        return coupon

    async def delete_coupon_admin(self, id: int, user_id: int, tenant_id: int) -> bool:
        coupon = await self.coupon_repository.delete_coupon_admin(id, user_id, tenant_id)
        return coupon
