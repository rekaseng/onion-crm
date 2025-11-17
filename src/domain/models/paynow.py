from pydantic import BaseModel


class Paynow(BaseModel):
    order_ref: str
    amount: float
