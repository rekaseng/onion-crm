from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from typing import Optional, List


class PaymentType(str, Enum):
    credit = "credit_card"
    coupon = "coupon"
    paynow = "paynow"
    wallet = "wallet"
    paynowBig  = "Paynow"  #todo:syd remove

class OrderItem(BaseModel):
    sku_sku: Optional[int] = None
    sku_id: int
    price: float
    quantity: int
    item_total: float
    sku_name: Optional[str] = None

    def to_dict(self):
        return self.dict()

    def attach_name(self, name: str):
        self.sku_name = name



class OrderPaymentItem(BaseModel):
    type: str
    amount: float

    def to_dict(self):
        return self.dict()


class OrderBase(BaseModel):
    id: Optional[int] = None
    order_ref: Optional[str] = None
    machine_id: Optional[int] = None
    subtotal: Optional[float] = None
    payment_amount: Optional[float] = None
    items: List[OrderItem]
    payments: List[OrderPaymentItem]
    is_deleted: bool = False
    user_id: Optional[int] = None
    tenant_id: Optional[int] = None
    machine_contract_id: Optional[int] = None

    def to_dict(self):
        return {
            **self.dict(),
            "items": [item.to_dict() for item in self.items],
            "payments": [payment.to_dict() for payment in self.payments],
        }


class Order(OrderBase):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    deleted_by: Optional[int] = None
