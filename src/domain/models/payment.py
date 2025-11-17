from enum import Enum
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class PaymentType(str, Enum):
    PAYNOW = "paynow"
    CREDIT_CARD = "credit_card"


class PaymentBase(BaseModel):
    user_id: Optional[int] = None
    order_id: Optional[int] = None
    transaction_id: Optional[int] = None
    amount: float
    type: Optional[str] = None
    description: Optional[str] = None
    invoice_no: str
    success: bool
    raw_data: Optional[dict] = None

class Payment(PaymentBase):
    id: Optional[int] = None
    is_deleted: bool = False
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[int] = None

    created_at: Optional[datetime]  = None
    created_by: Optional[int] = None

    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None
