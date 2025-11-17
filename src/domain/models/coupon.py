from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime, date


class CouponBase(BaseModel):
    id: Optional[int] = None
    name: str
    code: str
    discount_type: str
    discount_amount: float
    minimum_spending: float
    minimum_spending_active: bool
    criterial_cart_type: str
    criterial_cart_skus: List[int]
    criterial_cart_collections: List[int]
    active: bool
    target_type: str
    target_skus: List[int]
    target_collections: List[int]
    is_deleted: bool = False
    member_group_id: Optional[int] = None
    is_global: bool = False
    customer_limit: Optional[int] = None
    global_limit: Optional[int] = None
    date_start: Optional[date]
    date_end: Optional[date]


class Coupon(CouponBase):
    tenant_id: Optional[int] = None
    user_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    deleted_by: Optional[int] = None
