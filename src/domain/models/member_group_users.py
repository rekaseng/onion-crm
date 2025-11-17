from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class MemberGroupUsersBase(BaseModel):
    member_group_id: Optional[int] = None
    user_id: Optional[int] = None


class MemberGroupUsers(MemberGroupUsersBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_deleted: bool = False
    deleted_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    deleted_by: Optional[int] = None
