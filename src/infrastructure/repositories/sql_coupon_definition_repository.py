from typing import List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from datetime import datetime

from infrastructure.orm.orm_update_helper import update_orm_model_from_domain
from domain.models.coupon_definition import CouponDefinition, CouponDefinitionBase
from domain.repositories.coupon_definition_repository import CouponDefinitionRepository
from infrastructure.orm.coupon_definition_orm_model import CouponDefinitionOrmModel


class SQLCouponDefinitionRepository(CouponDefinitionRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all(self) -> List[CouponDefinition]:
        result = await self.db_session.execute(select(CouponDefinitionOrmModel).filter(CouponDefinitionOrmModel.is_deleted.is_(False)))
        orm_coupons = result.scalars().all()
        coupons = [item.to_domain() for item in orm_coupons]
        return coupons


    async def get_all_admin(self, tenant_id: int) -> List[CouponDefinition]:
        result = await self.db_session.execute(
            select(CouponDefinitionOrmModel).filter(CouponDefinitionOrmModel.tenant_id == tenant_id,
                                          CouponDefinitionOrmModel.is_deleted.is_(False)))
        orm_coupons = result.scalars().all()
        coupons = [item.to_domain() for item in orm_coupons]
        return coupons

    async def add(self, coupon: CouponDefinition) -> bool:
        coupon_result = await self.db_session.execute(select(CouponDefinitionOrmModel).filter_by(id=coupon.id))
        orm_coupon = coupon_result.scalars().first()

        if orm_coupon:
            raise HTTPException(status_code=400, detail="Coupon Definition with this id already exists")

        orm_coupon = CouponDefinitionOrmModel.from_domain(coupon)
        await self.db_session.merge(orm_coupon)
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            print(f"Database error occurred: {e}")
            return False

    async def get_by_ids(self, ids: List[int]) -> List[CouponDefinition]:
        query = select(CouponDefinitionOrmModel).filter(CouponDefinitionOrmModel.id.in_(ids), CouponDefinitionOrmModel.is_deleted.is_(False))
        result = await self.db_session.execute(query)
        orm_coupons = result.scalars().all()

        coupons = [item.to_domain() for item in orm_coupons]

        return coupons

    async def get_by_id(self, id: int) -> CouponDefinition:
        result = await self.db_session.execute(
            select(CouponDefinitionOrmModel).filter(CouponDefinitionOrmModel.id == id, CouponDefinitionOrmModel.is_deleted.is_(False)))
        orm_coupon = result.scalars().first()

        if orm_coupon is None:
            raise HTTPException(status_code=400, detail="Wrong Coupon Definition")

        coupon = orm_coupon.to_domain()
        return coupon

    async def get_by_id_admin(self, id: int, tenant_id: int) -> CouponDefinition:
        result = await self.db_session.execute(
            select(CouponDefinitionOrmModel).filter(CouponDefinitionOrmModel.tenant_id == tenant_id,
                                          CouponDefinitionOrmModel.id == id,
                                          CouponDefinitionOrmModel.is_deleted.is_(False)))
        orm_coupon = result.scalars().first()

        if orm_coupon is None:
            raise HTTPException(status_code=400, detail="Wrong Coupon Definition")

        coupon = orm_coupon.to_domain()
        return coupon

    async def update_coupon_definition(self, id:int, update_coupon: CouponDefinitionBase, user_id: int) -> bool:
        coupon_result = await self.db_session.execute(
            select(CouponDefinitionOrmModel).filter(CouponDefinitionOrmModel.id == id,
                                          CouponDefinitionOrmModel.is_deleted.is_(False)))
        orm_coupon = coupon_result.scalars().first()

        if orm_coupon is None:
            raise HTTPException(status_code=400, detail="Wrong Coupon Definition")
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

    async def update_coupon_definition_admin(self, id: int, update_coupon: CouponDefinitionBase, user_id: int, tenant_id: int) -> bool:
        coupon_result = await self.db_session.execute(
            select(CouponDefinitionOrmModel).filter(CouponDefinitionOrmModel.tenant_id == tenant_id,
                                          CouponDefinitionOrmModel.id == id,
                                          CouponDefinitionOrmModel.is_deleted.is_(False)))
        orm_coupon = coupon_result.scalars().first()

        if orm_coupon is None:
            raise HTTPException(status_code=400, detail="Wrong Coupon Definition")
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

    async def delete_coupon_definition(self, id: int, user_id: int) -> bool:
        coupon_result = await self.db_session.execute(
            select(CouponDefinitionOrmModel).filter(CouponDefinitionOrmModel.id == id, CouponDefinitionOrmModel.is_deleted.is_(False)))
        orm_coupon = coupon_result.scalars().first()

        if orm_coupon is None:
            raise HTTPException(status_code=400, detail="Wrong Coupon Definition")

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

    async def delete_coupon_definition_admin(self, id: int, user_id: int, tenant_id: int) -> bool:
        coupon_result = await self.db_session.execute(
            select(CouponDefinitionOrmModel).filter(CouponDefinitionOrmModel.tenant_id == tenant_id,
                                          CouponDefinitionOrmModel.id == id,
                                          CouponDefinitionOrmModel.is_deleted.is_(False)))
        orm_coupon = coupon_result.scalars().first()

        if orm_coupon is None:
            raise HTTPException(status_code=400, detail="Wrong Coupon Definition")

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