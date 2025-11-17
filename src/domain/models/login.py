from pydantic import BaseModel
from typing import Optional


class Login(BaseModel):
    mobile: str
    country_code: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class Message(BaseModel):
    message: str


class NewPassword(BaseModel):
    new_password: str
    otp: str
    full_mobile: str


class TokenPayload(BaseModel):
    sub: Optional[int] = None
    role_id: Optional[int] = None
    tenant_id: Optional[int] = None

