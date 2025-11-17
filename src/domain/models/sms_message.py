from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


class SmsMessage(BaseModel):
    full_mobile: str
    message_content: str

