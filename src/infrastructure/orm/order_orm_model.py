from _pydecimal import Decimal
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, DECIMAL, DateTime, func, ForeignKey, Boolean, String
from domain.models.order import Order, OrderItem, OrderPaymentItem, PaymentType
from infrastructure.db.base_class import Base
from sqlalchemy.dialects.postgresql import JSONB


class OrderOrmModel(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    user_id = Column(Integer, ForeignKey('users.id'))
    order_ref = Column(String(20))
    machine_id = Column(Integer)
    subtotal = Column(DECIMAL(15, 4), nullable=False)
    payment_amount = Column(DECIMAL(15, 4), nullable=False)
    items = Column(JSONB)
    payments = Column(JSONB)
    machine_contract_id = Column(Integer, ForeignKey('machine_contracts.id'))
    tenant_id = Column(Integer, ForeignKey('tenants.id'))
    is_deleted = Column(Boolean, nullable=False, default=False)
    deleted_at = Column(DateTime)
    created_by = Column(Integer, nullable=False, default=0)
    updated_by = Column(Integer, nullable=False, default=0)
    deleted_by = Column(Integer)

    @staticmethod
    def from_domain(order: Order):
        """Create an OrderOrmModel instance from an Order domain model."""
        order_dict = order.dict()
        return OrderOrmModel(
            **order_dict
        )

    def to_domain(self, sku_dict: Optional[dict] = None) -> Order:
        """Convert this OrderOrmModel instance to an Order domain model."""
        # Initialize order items
        order_items = [
            OrderItem(**item) for item in self.items
        ]

        # Attach names if sku_dict is provided
        if sku_dict:
            for item in order_items:
                if item.sku_id in sku_dict:
                    item.attach_name(sku_dict[item.sku_id]["name"])

        order = Order(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            user_id=self.user_id,
            subtotal=self.subtotal,
            payment_amount=self.payment_amount,
            items=order_items,
            payments=[OrderPaymentItem(**item) for item in self.payments],
            machine_contract_id=self.machine_contract_id,
            tenant_id=self.tenant_id,
            is_deleted=self.is_deleted,
            deleted_at=self.deleted_at,
            created_by=self.created_by,
            updated_by=self.updated_by,
            deleted_by=self.deleted_by
        )

        return order
