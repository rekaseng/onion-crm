from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from enum import Enum

class UserMessageBase(BaseModel):
    order_id: Optional[int] = None
    user_id: Optional[int] = None
    message: Optional[str] = None


class UserMessage(UserMessageBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
