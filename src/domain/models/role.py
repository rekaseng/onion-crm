from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


class RoleBase(BaseModel):
    name: str
    permissions: List[int]


class Role(RoleBase):
    id: Optional[int] = None
    tenant_id: Optional[int] = None
    is_admin: bool = False
    is_hq_admin: bool = False
    is_deleted: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    deleted_by: Optional[int] = None
