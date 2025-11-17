import os
from pathlib import Path
from typing import List

from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    POSTGRES_CONNECTION_STRING: str
    POSTGRES_SYNC_CONNECTION_STRING: str
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:3000"]
    CORS_ORIGIN_PATTERN: str
    PAYMENT_URL: str
    PAYMENT_MERCHANT_ID: str
    PAYMENT_MERCHANT_SHA: str
    PAYMENT_MERCHANT_CURRENCY_CODE:str
    PAYMENT_SUCCESS_URL: str
    RABBITMQ_HOST: str
    RABBITMQ_VIRTUAL_HOST: str
    RABBITMQ_PORT: str
    RABBITMQ_USERNAME: str
    RABBITMQ_PASSWORD: str
    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_PHONE_NUMBER: str
    HQ_URL: str
    HQ_API_KEY: str
    JWT_SECRET: str

    class Config:
        case_sensitive = True
        env_file = os.path.join(Path(__file__).resolve().parent.parent, '.env')
        env_file_encoding = 'utf-8'


def get_settings():
    # Set env to the value of PYTHON_ENV, defaulting to None if not set
    env = os.getenv('PYTHON_ENV')
    env_file = os.path.join(Path(__file__).resolve().parent.parent, '.env')

    if env == 'test':  # Switch to '.env.test' if PYTHON_ENV is 'test'
        env_file = '.env.test'

    return Settings(_env_file=env_file)

settings = get_settings()
