from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class UserQrKeysBase(BaseModel):
    name: str
    secret: str


class UserQrKeys(UserQrKeysBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_deleted: bool = False
    deleted_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    deleted_by: Optional[int] = None
    is_active: bool = False
