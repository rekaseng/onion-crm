from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class RefreshTokenBase(BaseModel):
    user_id: int
    refresh_token: str
    invalidate: bool
    expiry: datetime
    is_deleted: bool = False


class RefreshToken(RefreshTokenBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    deleted_by: Optional[int] = None
