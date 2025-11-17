from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class UserRoleBase(BaseModel):
    user_id: int
    role_id: int
    is_deleted: bool = False


class UserRole(UserRoleBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    deleted_by: Optional[int] = None
