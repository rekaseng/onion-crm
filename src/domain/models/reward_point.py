from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
class RewardPointBase(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    points: Optional[int] = None
    description: Optional[str] = None
    balance: Optional[int] = None
    order_id: Optional[int] = None
    type: Optional[str] = None
    transaction_at: Optional[datetime] = None

class RewardPoint(RewardPointBase):
    is_deleted: bool = False

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    deleted_by: Optional[int] = None

class RewardPointOption(BaseModel):
    point: Optional[int] = None
    discount: Optional[float] = None