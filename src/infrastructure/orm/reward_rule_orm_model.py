from _pydecimal import Decimal
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, DECIMAL, func, ForeignKey, Date
from domain.models.coupon import Coupon
from domain.models.reward_point import RewardPoint
from domain.models.reward_rule import RewardRule
from infrastructure.db.base_class import Base
from sqlalchemy.dialects.postgresql import JSONB

class RewardRuleOrmModel(Base):
    __tablename__ = "reward_rules"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    created_by = Column(Integer, nullable=False, default=0)
    updated_by = Column(Integer, nullable=False, default=0)
    deleted_by = Column(Integer)
    is_deleted = Column(Boolean, nullable=False, default=False)
    deleted_at = Column(DateTime)

    days = Column(JSONB)
    point_modifier = Column(Integer)


    @staticmethod
    def from_domain(reward_rule: RewardRule):
        """Create a CouponOrmModel instance from a Coupon domain model."""
        data_dict = reward_rule.dict()
        return RewardRuleOrmModel(
            **data_dict
        )

    def to_domain(self) -> RewardRule:
        """Convert this CouponOrmModel instance to a Coupon domain model."""
        return RewardRule(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,

            is_deleted=self.is_deleted,
            deleted_at=self.deleted_at,
            created_by=self.created_by,
            updated_by=self.updated_by,
            deleted_by=self.deleted_by,
            days=self.days,
            point_modifier=self.point_modifier
        )
