from http.client import HTTPException
from typing import List, Union

from application.dto.user_dto import MachineLoginWithUserDto
from domain.interfaces.ciper_interface import CipherInterface
from domain.models.login import Login
from typing import Optional
from domain.models.user import User, UserBase, UserUpdateDTO
from domain.repositories.hq_adapter import IHqAdapter
from domain.repositories.user_repository import UserRepository
from domain.repositories.auth_repository import AuthRepository
from application.dto.auth_dto import RegisterDTO
from utils.security import get_password_hash, sign_qr_payload
from datetime import datetime
from domain.repositories.otp_repository import OtpRepository
import re
from domain.models.user_message import UserMessage

def generate_slug(firstname: str, lastname: str) -> str:
    full_name = f"{firstname}-{lastname}"
    slug = full_name.lower().replace(" ", "-")
    slug = re.sub(r"[^a-z0-9-]", "", slug)
    return slug


class UserUseCases:
    def __init__(self,
                user_repository: UserRepository,
                auth_repository: Optional[AuthRepository],
                otp_repository: OtpRepository = None,
                cipher: CipherInterface = None,
                hq_adapter: IHqAdapter = None
        ):
        self.user_repository = user_repository
        self.auth_repository = auth_repository
        self.otp_repository = otp_repository
        self.cipher = cipher
        self.hq_adapter = hq_adapter

    async def add_user(self, user_dto: UserBase) -> bool:
        # Placeholder for password hashing logic
        hashed_password = get_password_hash(user_dto.password)
        full_mobile = f"{user_dto.country_code}{user_dto.mobile}"
        slug = generate_slug(user_dto.firstname, user_dto.lastname)

        user = User(
            created_at=datetime.now(),
            updated_at=datetime.now(),
            mobile=user_dto.mobile,
            country_code=user_dto.country_code,
            full_mobile=full_mobile,
            firstname=user_dto.firstname,
            lastname=user_dto.lastname,
            slug=slug,
            email=user_dto.email,
            birth_year=user_dto.birth_year,
            birth_month=user_dto.birth_month,
            birth_day=user_dto.birth_day,
            password=hashed_password,
            address=user_dto.address,
            postal_code=user_dto.postal_code,
            email_consent=user_dto.email_consent,
            sms_consent=user_dto.sms_consent,
            is_active=True,
            is_superuser=False,
            tenant_id=user_dto.tenant_id,
            is_deleted=False,
            deleted_at=None
        )
        await self.user_repository.add_user(user)
        return user

    async def add_user_admin(self, user_admin_dto: UserBase) -> bool:
        full_mobile = f"{user_admin_dto.country_code}{user_admin_dto.mobile}"
        hashed_password = get_password_hash(user_admin_dto.password)
        slug = generate_slug(user_admin_dto.firstname, user_admin_dto.lastname)
        user_admin = User(
            created_at=datetime.now(),
            updated_at=datetime.now(),
            mobile=user_admin_dto.mobile,
            country_code=user_admin_dto.country_code,
            full_mobile=full_mobile,
            firstname=user_admin_dto.firstname,
            lastname=user_admin_dto.lastname,
            slug=slug,
            email=user_admin_dto.email,
            birth_year=user_admin_dto.birth_year,
            birth_month=user_admin_dto.birth_month,
            birth_day=None,
            date_of_birth=None,
            password=hashed_password,
            address="",
            postal_code="",
            email_consent=False,
            sms_consent=False,
            is_active=True,
            is_superuser=False,
            tenant_id=user_admin_dto.tenant_id,
            is_deleted=False,
        )
        #await self.user_repository.add_user_admin(user_admin.tenant_id, user_admin)
        await self.user_repository.add_user(user_admin)
        return user_admin

    async def get_all(self, current_user: dict) -> List[User]:
        users = await self.user_repository.get_all(current_user)
        return users


    async def get_by_full_mobile(self, full_mobile: str) -> User:
        user = await self.user_repository.get_by_full_mobile(full_mobile)
        return user

    async def get_by_id(self, user_id: int) -> Union[User, None]:
        user = await self.user_repository.get_by_id(user_id)
        return user

    async def update_user_info(self, id: int, user_update_dto: UserUpdateDTO) -> bool:
        user = await self.user_repository.update_user_info(id, user_update_dto)
        return user

    async def delete_user(self, user_id: int, current_user: dict) -> bool:
        user = await self.user_repository.delete_user(user_id, current_user)
        return user

    async def get_profile(self, current_user: dict) -> Union[User, None]:
        user = await self.user_repository.get_profile(current_user)
        return user


    async def get_qr_code(self, current_user: dict) -> str:
        orm_active_key_name = await self.user_repository.get_active_key_name()
        key_name = orm_active_key_name
        orm_user_qr_key = await self.user_repository.get_user_qr_key(key_name)
        qr_payload = await self.user_repository.get_qr_code(current_user, key_name)

        signed_qr = sign_qr_payload(qr_payload, orm_user_qr_key.secret)
        user_qr_string = f"{qr_payload['user_id']}-{qr_payload['linked_credit_card']}-{qr_payload['store_credit_in_cents']}-{qr_payload['exp']}-{qr_payload['key_name']}-{signed_qr}"
        user_qr_string = self.cipher.encrypt(user_qr_string)

        user_qr_string = f"u-{user_qr_string}"

        return user_qr_string


    async def sign_up(self, register_dto: RegisterDTO) -> dict:
        full_mobile = register_dto.country_code + register_dto.mobile
        is_otp_valid = await self.otp_repository.verify(full_mobile, register_dto.otp)
        if not is_otp_valid:
            raise HTTPException(status_code=400, detail="Invalid OTP")

        hashed_password = get_password_hash(register_dto.password)
        slug = generate_slug(register_dto.firstname, register_dto.lastname)

        user = User(
            created_at=datetime.now(),
            updated_at=datetime.now(),
            mobile=register_dto.mobile,
            country_code=register_dto.country_code,
            full_mobile=full_mobile,
            firstname=register_dto.firstname,
            lastname=register_dto.lastname,
            slug=slug,
            email="",
            birth_year=None,
            birth_month=None,
            birth_day=None,
            date_of_birth=None,
            password=hashed_password,
            address="",
            postal_code="",
            email_consent=False,
            sms_consent=False,
            is_active=True,
            is_superuser=False,
            tenant_id=1,
            is_deleted=False,
        )

        await self.user_repository.register(user)

        login_data = Login(mobile=register_dto.mobile, country_code=register_dto.country_code,
                           password=register_dto.password)
        token = await self.auth_repository.login_access_token(login_data)

        return {"user": user, "token": token}


    async def send_login_to_hq(self, login_dto: MachineLoginWithUserDto) -> dict:
        response = await self.hq_adapter.machine_login(login_dto)
        return response

    async def save_message(self, user_id: int, order_id: Optional[int], message: str, admin_id: int) -> bool:
        user_message = UserMessage(
            created_at=datetime.now(),
            updated_at=datetime.now(),
            user_id=user_id,
            order_id=order_id,
            message=message,
            created_by=admin_id,
            updated_by=admin_id
        )

        await self.user_repository.save_message(user_message)
        return True

    async def get_user_messages(self, user_id: int) -> List[UserMessage]:
        messages = await self.user_repository.get_user_messages(user_id)
        return messages