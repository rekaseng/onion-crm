from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class TransactionBase(BaseModel):
    user_id: Optional[int] = None
    order_id: Optional[int] = None
    amount: Optional[float] = None
    is_paid: Optional[bool] = None
    payment_type: Optional[str] = None

class Transaction(TransactionBase):
    id: Optional[int] = None
    transaction_ref: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
