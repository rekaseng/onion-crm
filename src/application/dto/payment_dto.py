from typing import Optional

from pydantic import BaseModel


class UserPaymentDto(BaseModel):
    user_id: Optional[int] = None
    subtotal: Optional[float] = None
