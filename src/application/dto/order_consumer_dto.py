from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from domain.models.order import Order, OrderPaymentItem, OrderItem


class OrderConsumerItemDto(BaseModel):
    item_total: Optional[float] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    sku_id: Optional[int] = None

class OrderConsumerPaymentDto(BaseModel):
    type: Optional[str] = None
    amount: Optional[float] = None


class OrderConsumerCouponDto(BaseModel):
    coupon_id: Optional[int] = None
    member_group_coupon_id: Optional[int] = None
    user_coupon_id: Optional[int] = None
    spend_points: Optional[int] = None
    amount: Optional[float] = None

class OrderRewardPointDto(BaseModel):
    point: Optional[int] = None
    discount: Optional[float] = None

class OrderConsumerDto(BaseModel):
    machine_id: Optional[int] = None
    order_id: Optional[str] = None
    payment_type: Optional[str] = None
    items: List[OrderConsumerItemDto]
    transaction_at: Optional[datetime] = None
    user_id: Optional[int] = None
    subtotal: Optional[float] = None
    payments: Optional[List[OrderConsumerPaymentDto]] = None
    coupons: Optional[List[OrderConsumerCouponDto]] = None
    reward_points: Optional[List[OrderRewardPointDto]] = None

    def to_domain_order(self)-> Order:
        #single payment for now
        order_items = []
        for x in self.items:
            order_item = OrderItem(
                sku_id=x.sku_id,
                price=x.price,
                quantity=x.quantity,
                item_total=x.item_total
            )
            order_items.append(order_item)

        payment_items = []
        for x in self.payments:
            payment_item = OrderPaymentItem(
                type=x.type,
                amount=x.amount

            )
            payment_items.append(payment_item)

        order = Order(
            order_ref=self.order_id,
            user_id=self.user_id,
            machine_id=self.machine_id,
            subtotal=self.subtotal,
            items=order_items,
            payment_amount=self.subtotal,
            payments=payment_items
        )

        return order