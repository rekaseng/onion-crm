from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime, date


class CouponDefinitionBase(BaseModel):
    id: Optional[int] = None
    name: str
    code: str
    discount_type: str
    discount_amount: float
    minimum_spending: Optional[float] = None
    minimum_spending_active: bool
    criterial_cart_type: Optional[str] = None
    criterial_cart_skus: List[int]
    criterial_cart_collections: List[int]
    active: bool
    target_type: str
    target_skus: List[int]
    target_collections: List[int]
    is_deleted: bool = False
    is_global: bool = False


class CouponDefinition(CouponDefinitionBase):
    tenant_id: Optional[int] = None 
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    deleted_by: Optional[int] = None
