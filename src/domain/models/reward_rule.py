from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
class RewardRuleBase(BaseModel):
    id: Optional[int] = None
    days: List[int] = None
    point_modifier: int

class RewardRule(RewardRuleBase):
    is_deleted: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    deleted_by: Optional[int] = None