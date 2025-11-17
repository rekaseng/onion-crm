from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


class MemberGroupBase(BaseModel):
    name: str
    description: Optional[str] = None
    user_ids: Optional[List[int]] = None
    all_users: Optional[bool] = False

class MemberGroup(MemberGroupBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    tenant_id: Optional[int] = None
    slug: str
    is_active: bool = True
    is_global: bool = False
    is_deleted: bool = False
    deleted_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    deleted_by: Optional[int] = None
