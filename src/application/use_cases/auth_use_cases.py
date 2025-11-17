from domain.models.login import Login, Token, Message, NewPassword
from domain.repositories.auth_repository import AuthRepository
from domain.repositories.otp_repository import OtpRepository


class AuthUseCases:
    def __init__(self, auth_repository: AuthRepository, otp_repository: OtpRepository):
        self.auth_repository = auth_repository
        self.otp_repository = otp_repository


    async def login_access_token(self, form_data: Login) -> Token:
        token = await self.auth_repository.login_access_token(form_data)
        return token

    async def reset_password(self, full_mobile: str, otp: str, new_password: str) -> Message:
        is_otp_valid = await self.otp_repository.verify(full_mobile, otp)

        if not is_otp_valid:
            raise HTTPException(status_code=400,
                                detail="Invalid OTP")

        message = await self.auth_repository.reset_password(full_mobile, new_password)
        return message
