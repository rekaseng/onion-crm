from datetime import datetime, timedelta
from typing import Any, Optional, Union

from jose import ExpiredSignatureError, jwt
from passlib.context import CryptContext
import uuid
from config import settings

from domain.models.two_c_two_p_payments import TwoCTwoPPaymentResponse, TwoCTwoPPaymentResultResponse, TwoCTwoPRequestPaymentPayload

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"
# 525600 = 1 year
ACCESS_TOKEN_EXPIRE_MINUTES = 525600
SECRET_KEY = settings.JWT_SECRET


def create_access_token(subject: Union[str, Any], role_id: Union[str, Any], tenant_id: Union[str, Any], expires_delta: timedelta) -> str:
    expire = datetime.utcnow() + expires_delta
    to_encode = {"exp": expire, "sub": str(subject), "role_id": str(role_id), "tenant_id": str(tenant_id)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_payment_token(payload: TwoCTwoPRequestPaymentPayload) -> str:
    expire = datetime.utcnow() + timedelta(minutes=5)
    return jwt.encode({**payload.dict(), "exp": expire}, settings.PAYMENT_MERCHANT_SHA, algorithm='HS256')

def decode_payment_token(token: str) -> Optional[TwoCTwoPPaymentResponse]:
    try:
        decoded_token = jwt.decode(token, settings.PAYMENT_MERCHANT_SHA, algorithms=['HS256'])
        payload = TwoCTwoPPaymentResponse(
            webPaymentUrl = decoded_token['webPaymentUrl'],
            paymentToken = decoded_token['paymentToken'],
            respCode = decoded_token['respCode'],
            respDesc = decoded_token['respDesc'],
        )
        return payload
    except ExpiredSignatureError:
        print("Token has expired")
    return None

def decode_payment_result_token(token: str) -> Optional[TwoCTwoPPaymentResultResponse]:
    try:
        decoded_token = jwt.decode(token, settings.PAYMENT_MERCHANT_SHA, algorithms=['HS256'])
        payload = TwoCTwoPPaymentResultResponse(
            merchantID = decoded_token['merchantID'],
            invoiceNo = decoded_token['invoiceNo'],
            accountNo = decoded_token['accountNo'],
            amount = decoded_token['amount'],
            currencyCode = decoded_token['currencyCode'],
            tranRef = decoded_token['tranRef'],
            referenceNo = decoded_token['referenceNo'],
            approvalCode = decoded_token['approvalCode'],
            eci = decoded_token['eci'],
            transactionDateTime = decoded_token['transactionDateTime'],
            respCode = decoded_token['respCode'],
            respDesc = decoded_token['respDesc'],
            paymentScheme = decoded_token['paymentScheme'],
            childMerchantID = decoded_token['childMerchantID'],
            agentCode = decoded_token['agentCode'],
            channelCode = decoded_token['channelCode'],
            customerToken = decoded_token['customerToken'],
            customerTokenExpiry = decoded_token['customerTokenExpiry'],
            cardType = decoded_token['cardType'],
            issuerCountry = decoded_token['issuerCountry'],
            issuerBank = decoded_token['issuerBank'],
            paymentID = decoded_token['paymentID'],
            schemePaymentID = decoded_token['schemePaymentID']
        )
        return payload
    except ExpiredSignatureError:
        print("Token has expired")
    return None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def generate_uuid_slug(value: int):
    namespace = uuid.UUID('12345678-1234-5678-1234-567812345678')
    value_str = str(value)
    unique_uuid = uuid.uuid5(namespace, value_str)
    return str(unique_uuid)


def create_qr_payload(user_id: int, store_credit_in_cents: str, linked_credit_card: bool,  key_name: str, expiration_minutes: int = 3600000) -> dict:
    exp = datetime.now() + timedelta(minutes=expiration_minutes)
    payload = {
        "user_id": user_id,
        "store_credit_in_cents": store_credit_in_cents,
        "linked_credit_card": linked_credit_card,
        "exp": int(exp.timestamp()),
        "key_name": key_name
    }
    return payload


# Function to sign the payload
def sign_qr_payload(payload: dict, secret: str) -> str:
    signed_qr = jwt.encode(payload, secret, algorithm="HS256")
    print(signed_qr)
    part = signed_qr.split('.')
    truncated_signed_qr = part[2][:5]

    cleaned_truncated_signed_qr = truncated_signed_qr.replace('-', '')

    print(cleaned_truncated_signed_qr)
    return cleaned_truncated_signed_qr