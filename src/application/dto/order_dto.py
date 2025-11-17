from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from domain.models.order import Order, OrderPaymentItem, OrderItem


class OrderDeductAmountDto(BaseModel):
    customer_id: Optional[int] = None
    order_id: Optional[int] = None
    amount: Optional[float] = None
    description: Optional[str] = None

class OrderSendMessageDto(BaseModel):
    customer_id: Optional[int] = None
    message: Optional[str] = None
