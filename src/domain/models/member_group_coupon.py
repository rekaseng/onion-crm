from typing import Optional, List
from datetime import datetime, date
from pydantic import BaseModel


class MemberGroupCouponBase(BaseModel):
    id: Optional[int] = None
    member_group_id: Optional[int] = None
    coupon_definition_id: Optional[int] = None

    name: Optional[str] = None
    date_start: Optional[date] = None
    date_end: Optional[date] = None
    all_machines: bool = False
    applicable_machines: Optional[List[int]] = None

    user_redemption_period_limit: Optional[int] = None
    user_redemption_period_type: Optional[str] = None
    group_redemption_period_limit: Optional[int] = None
    group_redemption_period_type: Optional[str] = None


class MemberGroupCoupon(MemberGroupCouponBase):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    deleted_by: Optional[int] = None
    is_deleted: bool = False
