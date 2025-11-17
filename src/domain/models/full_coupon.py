from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime, date

from domain.models.coupon_definition import CouponDefinition


class  FullCoupon(CouponDefinition):
    # this model combines coupon_definition and part of user/member_group_coupons

    # properties for user criteria
    member_group_coupon_id:Optional[int] = None
    user_coupon_id:Optional[int] = None
    date_start: Optional[date] = None
    date_end: Optional[date] = None
    all_machines: bool = False
    applicable_machines: Optional[List[int]] = None
    user_redemption_period_limit: Optional[int] = None
    user_redemption_period_type: Optional[str] = None

