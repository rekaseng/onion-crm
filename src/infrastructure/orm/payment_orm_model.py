from sqlalchemy import Column, Float, ForeignKey, Integer, String, DateTime, Boolean
from domain.models.payment import Payment
from infrastructure.db.base_class import Base
from sqlalchemy.dialects.postgresql import JSONB


class PaymentOrmModel(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    order_id = Column(Integer, index=True)
    transaction_id = Column(Integer, index=True)

    type = Column(String(96))
    description = Column(String(400))
    invoice_no = Column(String, unique=True, nullable=False, index=True)
    amount = Column(Float, nullable=False)
    success = Column(Boolean, nullable=False, default=False)
    raw_data = Column(JSONB)
    is_deleted = Column(Boolean, nullable=False, default=False)
    deleted_at = Column(DateTime)
    deleted_by = Column(Integer)
    created_at = Column(DateTime)
    created_by = Column(Integer, nullable=False, default=0)
    updated_at = Column(DateTime)
    updated_by = Column(Integer, nullable=False, default=0)

    @staticmethod
    def from_domain(payment: Payment):
        """Create a PaymentOrmModel instance from a Payment domain model."""
        return PaymentOrmModel(
            id=payment.id,
            user_id=payment.user_id,
            order_id=payment.order_id,
            transaction_id = payment.transaction_id,
            type=payment.type,
            description=payment.description,
            invoice_no=payment.invoice_no,
            amount=payment.amount,
            success=payment.success,
            raw_data=payment.raw_data,
            is_deleted=payment.is_deleted,
            deleted_at=payment.deleted_at,
            deleted_by=payment.deleted_by,

            created_at=payment.created_at,
            created_by=payment.created_by,

            updated_at=payment.updated_at,
            updated_by=payment.updated_by,
        )

    def to_domain(self) -> Payment:
        """Convert this PaymentOrmModel instance to a Payment domain model."""
        return Payment(
            id=self.id,
            user_id=self.user_id,
            order_id=self.order_id,
            transaction_id=self.transaction_id,
            type=self.type,
            description=self.description,
            invoice_no=self.invoice_no,
            amount=self.amount,
            success=self.success,
            raw_data=self.raw_data,
            is_deleted=self.is_deleted,
            deleted_at=self.deleted_at,
            deleted_by=self.deleted_by,
            created_at=self.created_at,
            created_by=self.created_by,
            updated_at=self.updated_at,
            updated_by=self.updated_by,
        )
