from _pydecimal import Decimal
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, DECIMAL, func, ForeignKey, Date
from domain.models.coupon import Coupon
from infrastructure.db.base_class import Base
from sqlalchemy.dialects.postgresql import JSONB

class CouponOrmModel(Base): #todo: deprecated
    __tablename__ = "coupons"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    name = Column(String(128), nullable=False)
    code = Column(String(32), default=None)
    discount_type = Column(String(10), nullable=False)
    discount_amount = Column(DECIMAL(15, 4), nullable=False)
    minimum_spending = Column(DECIMAL(15, 4), nullable=False)
    minimum_spending_active = Column(Boolean)
    criterial_cart_type = Column(String(10), nullable=False)
    criterial_cart_skus = Column(JSONB)
    criterial_cart_collections = Column(JSONB)
    active = Column(Boolean)
    target_type = Column(String(10), nullable=False)
    customer_limit = Column(Integer)
    voucher_limit = Column(Integer)
    is_global = Column(Boolean, nullable=False, default=False)
    date_start = Column(Date)
    date_end = Column(Date)

    target_skus = Column(JSONB)
    target_collections = Column(JSONB)
    is_deleted = Column(Boolean, nullable=False, default=False)
    deleted_at = Column(DateTime)
    member_group_id = Column(Integer, ForeignKey('member_groups.id'))
    tenant_id = Column(Integer, ForeignKey('tenants.id'))
    created_by = Column(Integer, nullable=False, default=0)
    updated_by = Column(Integer, nullable=False, default=0)
    deleted_by = Column(Integer)

    @staticmethod
    def from_domain(coupon: Coupon):
        """Create a CouponOrmModel instance from a Coupon domain model."""
        coupon_dict = coupon.dict()
        return CouponOrmModel(
            **coupon_dict
        )

    def to_domain(self) -> Coupon:
        """Convert this CouponOrmModel instance to a Coupon domain model."""
        return Coupon(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            name=self.name,
            code=self.code,
            discount_type=self.discount_type,
            discount_amount=self.discount_amount,
            minimum_spending=self.minimum_spending,
            minimum_spending_active=self.minimum_spending_active,
            criterial_cart_type=self.criterial_cart_type,
            criterial_cart_skus=self.criterial_cart_skus,
            criterial_cart_collections=self.criterial_cart_collections,
            active=self.active,
            target_type=self.target_type,
            target_skus=self.target_skus,
            target_collections=self.target_collections,
            member_group_id=self.member_group_id,
            tenant_id=self.tenant_id,
            is_global=self.is_global,
            is_deleted=self.is_deleted,
            date_start=self.date_start,
            date_end = self.date_end,
            customer_limit=self.customer_limit,
            voucher_limit = self.voucher_limit,
            deleted_at=self.deleted_at,
            created_by=self.created_by,
            updated_by=self.updated_by,
            deleted_by=self.deleted_by
        )
