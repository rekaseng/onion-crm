from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    mobile: str
    country_code: str
    full_mobile: str
    firstname: str
    lastname: str
    email: str
    birth_year: Optional[int]
    birth_month: Optional[int]
    birth_day: Optional[int]
    password: str
    address: str
    postal_code: str
    email_consent: bool
    sms_consent: bool
    is_active: bool
    is_superuser: bool
    tenant_id: Optional[int] = None
    is_deleted: bool = False


class User(UserBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    slug: str
    deleted_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    deleted_by: Optional[int] = None
    credits: Optional[float] = 0.0


class UpdatePassword(BaseModel):
    email: str
    current_password: str
    new_password: str


class DeleteUser(BaseModel):
    email: EmailStr
    password: str


class UserUpdateDTO(BaseModel):
    mobile: str
    country_code: str
    full_mobile: str
    firstname: str
    lastname: str
    email: str
    birth_year: Optional[int]
    birth_month: Optional[int]
    email_consent: bool = False
    sms_consent: bool = False
