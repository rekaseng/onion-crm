from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class PaymentMethodBase(BaseModel):
    user_id: int
    payment_token: str
    card_type: Optional[str] = None
    card_last_four: Optional[str] = None
    expiry_date: Optional[datetime] = None

class PaymentMethod(PaymentMethodBase):
    id: Optional[int] = None
    is_deleted: bool = False
    deleted_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    deleted_by: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None