from pydantic import BaseModel

from domain.models.role import Role
from domain.models.tenant import Tenant
from domain.models.user import User


class RegisterDTO(BaseModel):
    mobile: str
    country_code: str
    password: str
    firstname: str
    lastname: str
    otp: str


class UserLoginDTO(BaseModel):
    mobile: str
    country_code: str
    password: str


class NewPasswordDTO(BaseModel):
    new_password: str
    otp: str
    full_mobile: str

class UserAuthDTO(BaseModel):
    user: User
    role: Role
    tenant: Tenant

class SendOtpDto(BaseModel):
    full_mobile: str

class OtpVerificationDto(BaseModel):
    first_name: str
    last_name: str
    password: str
    full_mobile: str
    otp: str
