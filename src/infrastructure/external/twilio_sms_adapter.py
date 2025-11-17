from http.client import HTTPException
from config import settings
from domain.models.sms_message import SmsMessage
from domain.repositories.sms_adapter import ISmsAdapter
from twilio.rest import Client as TwilioClient


class TwilioSmsAdapter(ISmsAdapter):
    def send_sms(self, message: SmsMessage) -> bool:
        account_sid = settings.TWILIO_ACCOUNT_SID
        auth_token = settings.TWILIO_AUTH_TOKEN
        from_number = settings.TWILIO_PHONE_NUMBER
        twilio_client = TwilioClient(account_sid, auth_token)
        try:
            twilio_client.messages.create(
                body=message.message_content,
                from_=from_number,
                to= message.full_mobile
            )
            print("sent: " , message.full_mobile)
        except Exception as e:
            print('error', e)
            raise HTTPException(status_code=500, detail=str(e))

        return True

