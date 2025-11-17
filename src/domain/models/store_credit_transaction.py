from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from enum import Enum


class StoreCreditTransactionType(str, Enum):
    CREDIT = "credit"
    DEBIT = "debit"


class StoreCreditTransactionBase(BaseModel):
    type: StoreCreditTransactionType
    order_id: Optional[int] = None
    user_id: Optional[int] = None
    description: Optional[str] = None
    amount: float
    is_deleted: bool = False


class StoreCreditTransaction(StoreCreditTransactionBase):
    id: Optional[int] = None
    store_credit_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    deleted_by: Optional[int] = None
