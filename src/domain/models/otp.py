from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


class Otp(BaseModel):
    id: Optional[int] = None  # Make id optional
    full_mobile: str
    otp: str
    attempts: Optional[int] = 0  # Make attempts optional
    created_at: datetime


