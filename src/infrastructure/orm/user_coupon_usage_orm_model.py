from _pydecimal import Decimal
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, DECIMAL, func, ForeignKey, Date
from domain.models.coupon import Coupon
from domain.models.coupon_definition import CouponDefinition
from domain.models.user_coupon_usage import UserCouponUsage
from infrastructure.db.base_class import Base
from sqlalchemy.dialects.postgresql import JSONB

class UserCouponUsageOrmModel(Base):
    __tablename__ = "user_coupon_usages"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    is_deleted = Column(Boolean, nullable=False, default=False)
    deleted_at = Column(DateTime)
    deleted_by = Column(Integer)

    user_id = Column(Integer, ForeignKey('users.id'))
    user_coupon_id= Column(Integer, ForeignKey('user_coupons.id'))
    member_group_coupon_id=Column(Integer, ForeignKey('member_group_coupons.id'))


    @staticmethod
    def from_domain(user_coupon_usage: UserCouponUsage):
        """Create a CouponOrmModel instance from a Coupon domain model."""
        user_coupon_usage_dict = user_coupon_usage.dict()
        return UserCouponUsageOrmModel(
            **user_coupon_usage_dict
        )

    def to_domain(self) -> UserCouponUsage:
        """Convert this CouponOrmModel instance to a Coupon domain model."""
        return UserCouponUsage(
            id=self.id,
            created_at=self.created_at,
            deleted_at=self.deleted_at,
            deleted_by=self.deleted_by,
            is_deleted=self.is_deleted,
            user_id = self.user_id,
            user_coupon_id=self.user_coupon_id,
            member_group_coupon_id=self.member_group_coupon_id,
        )
