from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr


class TenantBase(BaseModel):
    name: str
    main_contact_name: str
    main_contact_mobile: str
    main_contact_email: EmailStr
    main_contact_address: str
    admin: Optional[List[int]]
    is_deleted: bool = False


class Tenant(TenantBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    deleted_by: Optional[int] = None
