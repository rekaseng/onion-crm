
from sqlalchemy import Column, Integer, String, Boolean, DateTime, DECIMAL, func, ForeignKey, Date
from domain.models.reward_point import RewardPoint
from infrastructure.db.base_class import Base

class RewardPointOrmModel(Base):
    __tablename__ = "reward_points"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    created_by = Column(Integer, nullable=False, default=0)
    updated_by = Column(Integer, nullable=False, default=0)
    deleted_by = Column(Integer)
    is_deleted = Column(Boolean, nullable=False, default=False)
    deleted_at = Column(DateTime)

    user_id = Column(Integer)
    points = Column(Integer)
    description = Column(String(1000))
    balance = Column(Integer)
    order_id = Column(Integer)
    type = Column(String(40))
    transaction_at = Column(DateTime)


    @staticmethod
    def from_domain(reward_point: RewardPoint):
        """Create a CouponOrmModel instance from a Coupon domain model."""
        data_dict = reward_point.dict()
        return RewardPointOrmModel(
            id=reward_point.id,
            created_at=reward_point.created_at,
            updated_at=reward_point.updated_at,
            is_deleted=reward_point.is_deleted,
            deleted_at=reward_point.deleted_at,
            created_by=reward_point.created_by,
            updated_by=reward_point.updated_by,
            deleted_by=reward_point.deleted_by,

            user_id=reward_point.user_id,
            points=reward_point.points,
            balance=reward_point.balance,
            description=reward_point.description,
            order_id=reward_point.order_id,
            type=reward_point.type,
            transaction_at=reward_point.transaction_at.replace(tzinfo=None)

        )

    def to_domain(self) -> RewardPoint:
        """Convert this CouponOrmModel instance to a Coupon domain model."""
        return RewardPoint(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,

            is_deleted=self.is_deleted,
            deleted_at=self.deleted_at,
            created_by=self.created_by,
            updated_by=self.updated_by,
            deleted_by=self.deleted_by,

            user_id=self.user_id,
            points=self.points,
            balance=self.balance,
            description=self.description,
            order_id=self.order_id,
            type=self.type,
            transaction_at=self.transaction_at
        )
