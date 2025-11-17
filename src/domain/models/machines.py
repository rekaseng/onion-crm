from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class MachinesBase(BaseModel):
    name: str
    is_active: bool = True
    is_deleted: bool = False


class Machines(MachinesBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    deleted_by: Optional[int] = None
