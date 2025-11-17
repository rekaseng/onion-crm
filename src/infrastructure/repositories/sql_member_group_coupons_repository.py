from typing import List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from domain.models.member_group_coupon import MemberGroupCoupon, MemberGroupCouponBase
from domain.repositories.member_group_coupons_repository import MemberGroupCouponsRepository
from infrastructure.orm.coupon_definition_orm_model import CouponDefinitionOrmModel
from infrastructure.orm.member_group_coupons_orm_model import MemberGroupCouponOrmModel
from infrastructure.orm.coupon_orm_model import CouponOrmModel
from infrastructure.orm.member_groups_orm_model import MemberGroupOrmModel

from fastapi import HTTPException
from datetime import datetime

from infrastructure.orm.orm_update_helper import update_orm_model_from_domain


class SQLMemberGroupCouponsRepository(MemberGroupCouponsRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all(self, current_user: dict) -> List[MemberGroupCoupon]:
        result = await self.db_session.execute(
            select(MemberGroupCouponOrmModel).filter(MemberGroupCouponOrmModel.is_deleted.is_(False)))
        orm_member_group_coupons = result.scalars().all()
        member_group_coupons = [item.to_domain() for item in orm_member_group_coupons]
        return member_group_coupons

    async def get_all_admin(self, current_user: dict) -> List[MemberGroupCoupon]:
        result = await self.db_session.execute(
            select(MemberGroupCouponOrmModel)
            .join(MemberGroupOrmModel, MemberGroupCouponOrmModel.member_group_id == MemberGroupOrmModel.id)
            .filter(MemberGroupOrmModel.tenant_id == current_user["tenant"].id,
                    MemberGroupCouponOrmModel.is_deleted.is_(False))
        )
        orm_member_group_coupons = result.scalars().all()
        member_group_coupons = [item.to_domain() for item in orm_member_group_coupons]
        return member_group_coupons

    async def add(self, member_group_coupons: MemberGroupCoupon, current_user: dict) -> bool:
        coupon_result = await self.db_session.execute(
            select(CouponDefinitionOrmModel).filter_by(id=member_group_coupons.coupon_definition_id))
        orm_coupon = coupon_result.scalars().first()

        if not orm_coupon:
            raise HTTPException(status_code=400, detail="Wrong Coupon")

        member_groups_result = await self.db_session.execute(
            select(MemberGroupOrmModel).filter_by(id=member_group_coupons.member_group_id))
        orm_member_groups = member_groups_result.scalars().first()

        if not orm_member_groups:
            raise HTTPException(status_code=400, detail="Wrong MemberGroup")

        result = await self.db_session.execute(
            select(MemberGroupCouponOrmModel).filter(
                MemberGroupCouponOrmModel.coupon_definition_id == member_group_coupons.coupon_definition_id,
                MemberGroupCouponOrmModel.is_deleted.is_(False)))
        orm_member_group_coupon = result.scalars().first()

        if orm_member_group_coupon:
            raise HTTPException(status_code=400, detail="MemberGroupCoupon already exists")

        orm_member_group_coupon = MemberGroupCouponOrmModel.from_domain(member_group_coupons)
        await self.db_session.merge(orm_member_group_coupon)
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            print(f"Error committing to the database: {e}")
            return False

    async def add_admin(self, member_group_coupon: MemberGroupCoupon) -> bool:
        obj_in =  member_group_coupon
        coupon_definition_result = await self.db_session.execute(
            select(CouponDefinitionOrmModel).filter(CouponDefinitionOrmModel.id == obj_in.coupon_definition_id,
                                          CouponDefinitionOrmModel.is_deleted.is_(False)))
        orm_coupon_definition = coupon_definition_result.scalars().first()

        if not orm_coupon_definition:
            raise HTTPException(status_code=400, detail="Wrong Coupon")

        member_groups_result = await self.db_session.execute(
            select(MemberGroupOrmModel).filter(MemberGroupOrmModel.id == member_group_coupon.member_group_id,
                                               MemberGroupOrmModel.is_deleted.is_(False)))
        orm_member_group = member_groups_result.scalars().first()

        if not orm_member_group:
            raise HTTPException(status_code=400, detail="Wrong MemberGroup")

        result = await self.db_session.execute(
            select(MemberGroupCouponOrmModel)
            .join(MemberGroupOrmModel, MemberGroupCouponOrmModel.member_group_id == MemberGroupOrmModel.id)
            .filter(MemberGroupCouponOrmModel.coupon_definition_id == obj_in.coupon_definition_id,
                    MemberGroupCouponOrmModel.is_deleted.is_(False))
        )
        orm_member_group_coupons = result.scalars().first()

        if orm_member_group_coupons:
            raise HTTPException(status_code=400, detail="MemberGroupCoupon already exists")

        orm_member_group_coupons = MemberGroupCouponOrmModel.from_domain(obj_in)
        await self.db_session.merge(orm_member_group_coupons)
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False

    async def get_by_member_group_id(self, member_group_id: int, current_user: dict) -> List[MemberGroupCoupon]:
        member_groups_result = await self.db_session.execute(
            select(MemberGroupOrmModel).filter_by(id=member_group_id))
        orm_member_groups = member_groups_result.scalars().first()

        if not orm_member_groups:
            raise HTTPException(status_code=400, detail="Wrong MemberGroup")

        result = await self.db_session.execute(
            select(MemberGroupCouponOrmModel).filter(MemberGroupCouponOrmModel.member_group_id == member_group_id,
                                                     MemberGroupCouponOrmModel.is_deleted.is_(False)))
        orm_member_group_coupons = result.scalars().all()

        if orm_member_group_coupons is None:
            raise HTTPException(status_code=400, detail="Wrong MemberGroupCoupon")

        member_group_coupons = [item.to_domain() for item in orm_member_group_coupons]
        return member_group_coupons
    
    async def get_by_member_group_ids(self, member_group_ids: List[int]) -> List[MemberGroupCoupon]:
        result = await self.db_session.execute(
            select(MemberGroupCouponOrmModel).filter(MemberGroupCouponOrmModel.member_group_id.in_(member_group_ids),
                                                     MemberGroupCouponOrmModel.is_deleted.is_(False)))
        orm_member_group_coupons = result.scalars().all()

        if orm_member_group_coupons is None:
            raise HTTPException(status_code=400, detail="Wrong MemberGroupCoupon")

        member_group_coupons = [item.to_domain() for item in orm_member_group_coupons]
        return member_group_coupons

    async def get_by_member_group_coupon_id_admin(self, member_group_coupon_id: int, current_user: dict) -> MemberGroupCoupon:
        result = await self.db_session.execute(
            select(MemberGroupCouponOrmModel)
            .join(MemberGroupOrmModel, MemberGroupCouponOrmModel.member_group_id == MemberGroupOrmModel.id)
            .filter(MemberGroupOrmModel.tenant_id == current_user["tenant"].id,
                    MemberGroupCouponOrmModel.id == member_group_coupon_id,
                    MemberGroupCouponOrmModel.is_deleted.is_(False))
        )

        orm_member_group_coupon = result.scalars().first()

        if orm_member_group_coupon is None:
            raise HTTPException(status_code=400, detail="Wrong MemberGroupCoupon")

        member_group_coupons = orm_member_group_coupon.to_domain()
        return member_group_coupons

    async def update_member_group_coupon(self, update_member_group_coupons: MemberGroupCoupon, current_user: dict) -> bool:
        coupon_result = await self.db_session.execute(
            select(CouponOrmModel).filter_by(id=update_member_group_coupons.coupon_id))
        orm_coupon = coupon_result.scalars().first()

        if not orm_coupon:
            raise HTTPException(status_code=400, detail="Wrong Coupon")

        member_groups_result = await self.db_session.execute(
            select(MemberGroupOrmModel).filter_by(id=update_member_group_coupons.member_group_id))
        orm_member_groups = member_groups_result.scalars().first()

        if not orm_member_groups:
            raise HTTPException(status_code=400, detail="Wrong MemberGroup")

        member_group_coupons_result = await self.db_session.execute(
            select(MemberGroupCouponOrmModel).filter(
                MemberGroupCouponOrmModel.member_group_id == update_member_group_coupons.member_group_id,
                MemberGroupCouponOrmModel.is_deleted.is_(False)))
        orm_member_group_coupons = member_group_coupons_result.scalars().first()

        if orm_member_group_coupons is None:
            raise HTTPException(status_code=400, detail="Wrong MemberGroupCoupon")

        orm_member_group_coupons = update_orm_model_from_domain(orm_member_group_coupons,
                                                                update_member_group_coupons)
        orm_member_group_coupons.updated_at = datetime.now()
        orm_member_group_coupons.created_by = current_user["user"].id
        orm_member_group_coupons.updated_by = current_user["user"].id
        orm_member_group_coupons.deleted_by = None
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False

    async def update_member_group_coupon_admin(self, update_member_group_coupons: MemberGroupCoupon,
                                               current_user: dict) -> bool:
        coupon_result = await self.db_session.execute(
            select(CouponOrmModel).filter_by(id=update_member_group_coupons.coupon_id))
        orm_coupon = coupon_result.scalars().first()

        if not orm_coupon:
            raise HTTPException(status_code=400, detail="Wrong Coupon")

        member_group_result = await self.db_session.execute(
            select(MemberGroupCouponOrmModel).filter(
                MemberGroupOrmModel.id == update_member_group_coupons.member_group_id,
                MemberGroupOrmModel.tenant_id == current_user["tenant"].id,
                MemberGroupCouponOrmModel.is_deleted.is_(False)))
        orm_member_group = member_group_result.scalars().first()

        if not orm_member_group:
            raise HTTPException(status_code=400, detail="Wrong MemberGroup")

        result = await self.db_session.execute(
            select(MemberGroupCouponOrmModel)
            .join(MemberGroupOrmModel, MemberGroupCouponOrmModel.member_group_id == MemberGroupOrmModel.id)
            .filter(MemberGroupOrmModel.tenant_id == current_user["tenant"].id,
                    MemberGroupCouponOrmModel.coupon_id == update_member_group_coupons.coupon_id,
                    MemberGroupCouponOrmModel.is_deleted.is_(False))
        )
        orm_member_group_coupon = result.scalars().first()

        if orm_member_group_coupon is None:
            raise HTTPException(status_code=400, detail="Wrong MemberGroupCoupon")

        orm_member_group_coupon = update_orm_model_from_domain(orm_member_group_coupon,
                                                                update_member_group_coupons)
        orm_member_group_coupon.updated_at = datetime.now()
        orm_member_group_coupon.created_by = current_user["user"].id
        orm_member_group_coupon.updated_by = current_user["user"].id
        orm_member_group_coupon.deleted_by = None
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False

    async def delete_member_group_coupon(self, member_group_coupon_id: int, current_user: dict) -> bool:
        member_group_coupons_result = await self.db_session.execute(
            select(MemberGroupCouponOrmModel).filter(MemberGroupCouponOrmModel.id == member_group_coupon_id,
                                                     MemberGroupCouponOrmModel.is_deleted.is_(False)))
        orm_member_group_coupon = member_group_coupons_result.scalars().first()

        if orm_member_group_coupon is None:
            raise HTTPException(status_code=400, detail="Wrong MemberGroupCoupon")

        orm_member_group_coupon.updated_at = datetime.now()
        orm_member_group_coupon.is_deleted = True
        orm_member_group_coupon.deleted_at = datetime.now()
        orm_member_group_coupon.created_by = current_user["user"].id
        orm_member_group_coupon.updated_by = current_user["user"].id
        orm_member_group_coupon.deleted_by = current_user["user"].id
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False

    async def delete_member_group_coupon_admin(self, member_group_coupon_id: int, current_user: dict) -> bool:
        result = await self.db_session.execute(
            select(MemberGroupCouponOrmModel)
            .join(MemberGroupOrmModel, MemberGroupCouponOrmModel.member_group_id == MemberGroupOrmModel.id)
            .filter(MemberGroupOrmModel.tenant_id == current_user["tenant"].id,
                    MemberGroupCouponOrmModel.id == member_group_coupon_id,
                    MemberGroupCouponOrmModel.is_deleted.is_(False))
        )
        orm_member_group_coupon = result.scalars().first()

        if orm_member_group_coupon is None:
            raise HTTPException(status_code=400, detail="Wrong MemberGroupCoupon")

        orm_member_group_coupon.updated_at = datetime.now()
        orm_member_group_coupon.is_deleted = True
        orm_member_group_coupon.deleted_at = datetime.now()
        orm_member_group_coupon.created_by = current_user["user"].id
        orm_member_group_coupon.updated_by = current_user["user"].id
        orm_member_group_coupon.deleted_by = current_user["user"].id
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False
