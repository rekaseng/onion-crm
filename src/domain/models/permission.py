from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class PermissionBase(BaseModel):
    name: str


class Permission(PermissionBase):
    id: Optional[int] = None
    is_deleted: bool = False
    deleted_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    deleted_by: Optional[int] = None
