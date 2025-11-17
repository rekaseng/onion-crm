from typing import List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from datetime import datetime

from domain.repositories.user_coupon_usage_repository import UserCouponUsageRepository
from domain.models.user_coupon_usage import UserCouponUsage
from infrastructure.orm.user_coupon_usage_orm_model import UserCouponUsageOrmModel


class SQLUserCouponUsageRepository(UserCouponUsageRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all(self) -> List[UserCouponUsage]:
        result = await self.db_session.execute(select(UserCouponUsageOrmModel).filter(UserCouponUsageOrmModel.is_deleted.is_(False)))
        orm_coupons = result.scalars().all()
        coupons = [item.to_domain() for item in orm_coupons]
        return coupons


    def add(self, user_coupon_usage: UserCouponUsage) -> bool:
        pass

    async def get_by_user_id(self, user_id: int) -> List[UserCouponUsage]:
        result = await self.db_session.execute(select(UserCouponUsageOrmModel).filter(UserCouponUsageOrmModel.user_id == user_id, UserCouponUsageOrmModel.is_deleted.is_(False)))
        orm_coupons = result.scalars().all()
        coupons = [item.to_domain() for item in orm_coupons]
        return coupons

    