import json
from sqlalchemy import Column, Integer, String, DateTime, Date, func, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB

from domain.models.member_group_users import MemberGroupUsers
from domain.models.user_coupon import UserCoupon
from infrastructure.db.base_class import Base


class UserCouponOrmModel(Base):
    __tablename__ = "user_coupons"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    is_deleted = Column(Boolean, nullable=False, default=False)
    deleted_at = Column(DateTime)
    created_by = Column(Integer, nullable=False, default=0)
    updated_by = Column(Integer, nullable=False, default=0)
    deleted_by = Column(Integer)

    user_id = Column(Integer, ForeignKey('users.id'))
    coupon_definition_id = Column(Integer, ForeignKey('coupons.id'))

    name = Column(String(256))
    date_start = Column(Date)
    date_end = Column(Date)
    user_redemption_period_limit = Column(Integer)
    user_redemption_period_type = Column(String)
    all_machines = Column(Boolean)
    applicable_machines = Column(JSONB)




    @staticmethod
    def from_domain(obj_in: UserCoupon):
        orm = UserCouponOrmModel()
        orm.id=obj_in.id
        orm.created_at=obj_in.created_at
        orm.updated_at=obj_in.updated_at
        orm.is_deleted=obj_in.is_deleted
        orm.deleted_at=obj_in.deleted_at
        orm.created_by=obj_in.created_by
        orm.updated_by=obj_in.updated_by
        orm.deleted_by=obj_in.deleted_by

        orm.user_id=obj_in.user_id
        orm.coupon_definition_id = obj_in.coupon_definition_id

        orm.name = obj_in.name
        orm.date_start = obj_in.date_start
        orm.date_end = obj_in.date_end
        orm.user_redemption_period_limit = obj_in.user_redemption_period_limit
        orm.user_redemption_period_type = obj_in.user_redemption_period_type
        orm.all_machines = obj_in.all_machines
        orm.applicable_machines = obj_in.applicable_machines
        return orm


    def to_domain(self) -> UserCoupon:
        """Convert this MemberGroupUsersOrmModel instance to a MemberGroupUsers domain model."""
        return UserCoupon(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            is_deleted=self.is_deleted,
            deleted_at=self.deleted_at,
            created_by=self.created_by,
            updated_by=self.updated_by,
            deleted_by=self.deleted_by,

            user_id = self.user_id,
            coupon_definition_id = self.coupon_definition_id,

            name = self.name,
            date_start = self.date_start,
            date_end = self.date_end,
            user_redemption_period_limit = self.user_redemption_period_limit,
            user_redemption_period_type = self.user_redemption_period_type,
            all_machines = self.all_machines,
            applicable_machines = [int(value) for value in self.applicable_machines] if self.applicable_machines != None else [],
        )
