from typing import Optional, List
from datetime import datetime, date
from pydantic import BaseModel

class UserCouponUsageBase(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    user_coupon_id: Optional[int] = None
    member_group_coupon_id: Optional[int] = None

class UserCouponUsage(UserCouponUsageBase):
    created_at: Optional[datetime] = None
    is_deleted: bool = False
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[int] = None
