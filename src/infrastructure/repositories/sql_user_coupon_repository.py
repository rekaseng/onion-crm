from datetime import datetime
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from domain.models.coupon import Coupon
from domain.models.user_coupon import UserCoupon, UserCouponBase
from domain.repositories.user_coupon_repository import UserCouponRepository
from infrastructure.orm.coupon_orm_model import CouponOrmModel

from infrastructure.orm.user_coupon_orm_model import UserCouponOrmModel
from infrastructure.orm.orm_update_helper import update_orm_model_from_domain


class SQLUserCouponRepository(UserCouponRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_by_user_id(self, user_id: int) -> List[Coupon]:
        query = select(CouponOrmModel).filter(
            UserCouponOrmModel.is_deleted.is_(False),
            UserCouponOrmModel.user_id == user_id
        )

        result = await self.db_session.execute(query)
        orm_coupons = result.scalars().all()
        coupons = [item.to_domain() for item in orm_coupons]
        return coupons
    
    async def add(self, coupon: UserCoupon) -> bool:
        coupon_result = await self.db_session.execute(select(UserCouponOrmModel).filter_by(id=coupon.id))
        orm_coupon = coupon_result.scalars().first()

        if orm_coupon:
            raise HTTPException(status_code=400, detail="User Coupon with this id already exists")

        orm_coupon = UserCouponOrmModel.from_domain(coupon)
        await self.db_session.merge(orm_coupon)
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False

    async def get_by_id(self, id: int) -> Optional[UserCoupon]:
        result = await self.db_session.execute(
            select(UserCouponOrmModel).filter(UserCouponOrmModel.id == id, UserCouponOrmModel.is_deleted.is_(False)))
        orm_coupon = result.scalars().first()

        if orm_coupon is None:
            raise HTTPException(status_code=400, detail="Wrong User Coupon")

        coupon = orm_coupon.to_domain()
        return coupon
    
    async def get_user_coupon_by_user_id(self, user_id: int) -> List[UserCoupon]:
        result = await self.db_session.execute(
            select(UserCouponOrmModel).filter(UserCouponOrmModel.user_id == user_id, UserCouponOrmModel.is_deleted.is_(False)))
        orm_coupons = result.scalars().all()

        return [item.to_domain() for item in orm_coupons]

    async def get_by_ids(self, ids: List[int]) -> List[UserCoupon]:
        query = select(UserCouponOrmModel).filter(UserCouponOrmModel.id.in_(ids), UserCouponOrmModel.is_deleted.is_(False))
        result = await self.db_session.execute(query)
        orm_coupons = result.scalars().all()

        coupons = [item.to_domain() for item in orm_coupons]

        return coupons

    async def get_all(self) -> List[UserCoupon]:
        result = await self.db_session.execute(select(UserCouponOrmModel).filter(UserCouponOrmModel.is_deleted.is_(False)))
        orm_coupons = result.scalars().all()
        coupons = [item.to_domain() for item in orm_coupons]
        return coupons

    async def update_user_coupon(self, id: int, coupon_update_dto: UserCouponBase, user_id: int) -> bool:
        coupon_result = await self.db_session.execute(
            select(UserCouponOrmModel).filter(UserCouponOrmModel.id == id,
                                          UserCouponOrmModel.is_deleted.is_(False)))
        orm_coupon = coupon_result.scalars().first()

        if orm_coupon is None:
            raise HTTPException(status_code=400, detail="Wrong User Coupon")
        orm_coupon = update_orm_model_from_domain(orm_coupon, coupon_update_dto)
        orm_coupon.updated_at = datetime.now()
        orm_coupon.updated_by = user_id
        orm_coupon.deleted_by = None
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False

    async def delete_user_coupon(self, id: int, user_id: int) -> bool:
        coupon_result = await self.db_session.execute(
            select(UserCouponOrmModel).filter(UserCouponOrmModel.id == id, UserCouponOrmModel.is_deleted.is_(False)))
        orm_coupon = coupon_result.scalars().first()

        if orm_coupon is None:
            raise HTTPException(status_code=400, detail="Wrong User Coupon")

        orm_coupon.updated_at = datetime.now()
        orm_coupon.is_deleted = True
        orm_coupon.deleted_at = datetime.now()
        orm_coupon.updated_by = user_id
        orm_coupon.deleted_by = user_id
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False

