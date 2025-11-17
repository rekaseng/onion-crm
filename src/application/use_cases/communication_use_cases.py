from typing import Optional
from datetime import datetime, timedelta

from application.dto.auth_dto import OtpVerificationDto
from domain.models.otp import Otp
from domain.models.sms_message import SmsMessage
from domain.repositories.otp_repository import OtpRepository
import random

from domain.repositories.sms_adapter import ISmsAdapter


class CommunicationUseCases:
    def __init__(self, sms_adapter: ISmsAdapter):
        self.sms_adapter = sms_adapter

    async def send_message(self, full_mobile: str, message: str) -> bool:

        sms_message = SmsMessage(
            full_mobile=full_mobile,
            message_content=message
        )
        self.sms_adapter.send_sms(sms_message)

        return True