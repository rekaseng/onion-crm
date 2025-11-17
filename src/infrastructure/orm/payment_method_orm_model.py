from sqlalchemy import Column, Float, ForeignKey, Integer, String, DateTime, Boolean
from domain.models.payment import Payment
from infrastructure.db.base_class import Base
from sqlalchemy.dialects.postgresql import JSONB

from domain.models.payment_method import PaymentMethod


class PaymentMethodOrmModel(Base):
    __tablename__ = "payment_methods"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, default=0)
    payment_token = Column(String, nullable=True, unique=False)
    card_type = Column(String, nullable=False)
    card_last_four = Column(String, nullable=False)
    expiry_date = Column(DateTime, nullable=True)
    is_deleted = Column(Boolean, nullable=False, default=False)
    deleted_at = Column(DateTime)
    created_by = Column(Integer, nullable=False, default=0)
    updated_by = Column(Integer, nullable=False, default=0)
    deleted_by = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    @staticmethod
    def from_domain(paymentMethod: PaymentMethod):
        """Create a PaymentMethodOrmModel instance from a PaymentMethod domain model."""
        return PaymentMethodOrmModel(
            id=paymentMethod.id,
            user_id=paymentMethod.user_id,
            payment_token=paymentMethod.payment_token,
            card_type=paymentMethod.card_type,
            card_last_four=paymentMethod.card_last_four,
            expiry_date=paymentMethod.expiry_date,
            is_deleted=paymentMethod.is_deleted,
            deleted_at=paymentMethod.deleted_at,
            created_by=paymentMethod.created_by,
            updated_by=paymentMethod.updated_by,
            deleted_by=paymentMethod.deleted_by,
            updated_at=paymentMethod.updated_at,
            created_at=paymentMethod.created_at
        )

    def to_domain(self) -> PaymentMethod:
        """Convert this PaymentMethodOrmModel instance to a PaymentMethod domain model."""
        return PaymentMethod(
            id=self.id,
            user_id=self.user_id,
            payment_token=self.payment_token,
            card_type=self.card_type,
            card_last_four=self.card_last_four,
            expiry_date=self.expiry_date,
            is_deleted=self.is_deleted,
            deleted_at=self.deleted_at,
            created_by=self.created_by,
            updated_by=self.updated_by,
            deleted_by=self.deleted_by,
            updated_at=self.updated_at,
            created_at=self.created_at
        )
