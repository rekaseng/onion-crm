from typing import List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from domain.models.coupon import Coupon, CouponBase
from domain.repositories.coupon_repository import CouponRepository
from infrastructure.orm.coupon_orm_model import CouponOrmModel
from fastapi import HTTPException
from datetime import datetime

from infrastructure.orm.orm_update_helper import update_orm_model_from_domain


class SQLCouponRepository(CouponRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all(self) -> List[Coupon]:
        result = await self.db_session.execute(select(CouponOrmModel).filter(CouponOrmModel.is_deleted.is_(False)))
        orm_coupons = result.scalars().all()
        coupons = [item.to_domain() for item in orm_coupons]
        return coupons


    async def get_all_admin(self, tenant_id: int) -> List[Coupon]:
        result = await self.db_session.execute(
            select(CouponOrmModel).filter(CouponOrmModel.tenant_id == tenant_id,
                                          CouponOrmModel.is_deleted.is_(False)))
        orm_coupons = result.scalars().all()
        coupons = [item.to_domain() for item in orm_coupons]
        return coupons

    async def add(self, coupon: Coupon) -> bool:
        coupon_result = await self.db_session.execute(select(CouponOrmModel).filter_by(id=coupon.id))
        orm_coupon = coupon_result.scalars().first()

        if orm_coupon:
            raise HTTPException(status_code=400, detail="Coupon with this id already exists")

        orm_coupon = CouponOrmModel.from_domain(coupon)
        await self.db_session.merge(orm_coupon)
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False

    async def get_by_ids(self, ids: List[int]) -> List[Coupon]:
        query = select(CouponOrmModel).filter(CouponOrmModel.id.in_(ids), CouponOrmModel.is_deleted.is_(False))
        result = await self.db_session.execute(query)
        orm_coupons = result.scalars().all()

        coupons = [item.to_domain() for item in orm_coupons]

        return coupons

    async def get_by_id(self, id: int) -> Coupon:
        result = await self.db_session.execute(
            select(CouponOrmModel).filter(CouponOrmModel.id == id, CouponOrmModel.is_deleted.is_(False)))
        orm_coupon = result.scalars().first()

        if orm_coupon is None:
            raise HTTPException(status_code=400, detail="Wrong Coupon")

        coupon = orm_coupon.to_domain()
        return coupon

    async def get_by_id_admin(self, id: int, tenant_id: int) -> Coupon:
        result = await self.db_session.execute(
            select(CouponOrmModel).filter(CouponOrmModel.tenant_id == tenant_id,
                                          CouponOrmModel.id == id,
                                          CouponOrmModel.is_deleted.is_(False)))
        orm_coupon = result.scalars().first()

        if orm_coupon is None:
            raise HTTPException(status_code=400, detail="Wrong Coupon")

        coupon = orm_coupon.to_domain()
        return coupon

    async def update_coupon(self, id:int, update_coupon: CouponBase, user_id: int) -> bool:
        coupon_result = await self.db_session.execute(
            select(CouponOrmModel).filter(CouponOrmModel.id == id,
                                          CouponOrmModel.is_deleted.is_(False)))
        orm_coupon = coupon_result.scalars().first()

        if orm_coupon is None:
            raise HTTPException(status_code=400, detail="Wrong Coupon")
        orm_coupon = update_orm_model_from_domain(orm_coupon, update_coupon)
        orm_coupon.updated_at = datetime.now()
        orm_coupon.updated_by = user_id
        orm_coupon.deleted_by = None
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False

    async def update_coupon_admin(self, id: int, update_coupon: CouponBase, user_id: int, tenant_id: int) -> bool:
        coupon_result = await self.db_session.execute(
            select(CouponOrmModel).filter(CouponOrmModel.tenant_id == tenant_id,
                                          CouponOrmModel.id == id,
                                          CouponOrmModel.is_deleted.is_(False)))
        orm_coupon = coupon_result.scalars().first()

        if orm_coupon is None:
            raise HTTPException(status_code=400, detail="Wrong Coupon")
        orm_coupon = update_orm_model_from_domain(orm_coupon, update_coupon)
        orm_coupon.updated_at = datetime.now()
        orm_coupon.updated_by = user_id
        orm_coupon.deleted_by = None
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False

    async def delete_coupon(self, id: int, user_id: int) -> bool:
        coupon_result = await self.db_session.execute(
            select(CouponOrmModel).filter(CouponOrmModel.id == id, CouponOrmModel.is_deleted.is_(False)))
        orm_coupon = coupon_result.scalars().first()

        if orm_coupon is None:
            raise HTTPException(status_code=400, detail="Wrong Coupon")

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

    async def delete_coupon_admin(self, id: int, user_id: int, tenant_id: int) -> bool:
        coupon_result = await self.db_session.execute(
            select(CouponOrmModel).filter(CouponOrmModel.tenant_id == tenant_id,
                                          CouponOrmModel.id == id,
                                          CouponOrmModel.is_deleted.is_(False)))
        orm_coupon = coupon_result.scalars().first()

        if orm_coupon is None:
            raise HTTPException(status_code=400, detail="Wrong Coupon")

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