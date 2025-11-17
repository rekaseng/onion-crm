from typing import Optional
from datetime import datetime
from pydantic import BaseModel

from domain.models.store_credit_transaction import StoreCreditTransactionType


class StoreCreditBase(BaseModel):
    user_id: Optional[int] = None
    balance: Optional[float] = None
    is_deleted: bool
    latest_amount: Optional[float] = None
    type: Optional[StoreCreditTransactionType] = None

class StoreCredit(StoreCreditBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    deleted_by: Optional[int] = None
