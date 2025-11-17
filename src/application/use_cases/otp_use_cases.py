from typing import Optional
from datetime import datetime, timedelta

from application.dto.auth_dto import OtpVerificationDto
from domain.models.otp import Otp
from domain.models.sms_message import SmsMessage
from domain.repositories.otp_repository import OtpRepository
import random

from domain.repositories.sms_adapter import ISmsAdapter


class OtpUseCases:
    def __init__(self, otp_repository: OtpRepository, sms_adapter: ISmsAdapter):
        self.otp_repository = otp_repository
        self.sms_adapter = sms_adapter

    async def send_otp(self, full_mobile: str) -> Otp:
        otp_data = Otp(
            full_mobile=full_mobile,
            otp=str(int(random.randint(100000, 999999))),
            created_at=datetime.utcnow()
        )
        await self.otp_repository.add(otp_data)

        sms_message = SmsMessage(
            full_mobile=full_mobile,
            message_content='Your otp is ' + otp_data.otp
        )
        self.sms_adapter.send_sms(sms_message)

        return otp_data

    async def verify(self, otp_verification: OtpVerificationDto) -> bool :
        result = await self.otp_repository.verify(otp_verification)
        return result