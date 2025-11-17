from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, func
from infrastructure.db.base_class import Base
from domain.models.transaction import Transaction  # Import the domain model

class TransactionOrmModel(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    user_id = Column(Integer, index=True, nullable=True)
    order_id = Column(Integer, index=True, nullable=True)
    amount = Column(Float, nullable=False)
    is_paid = Column(Boolean, nullable=False)
    payment_type = Column(String, nullable=False)
    transaction_ref = Column(String, unique=True, nullable=True)
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)

    @staticmethod
    def from_domain(transaction: Transaction):
        return TransactionOrmModel(
            created_at=transaction.created_at,
            updated_at=transaction.updated_at,
            user_id=transaction.user_id,
            order_id=transaction.order_id,
            amount=transaction.amount,
            is_paid=transaction.is_paid,
            payment_type=transaction.payment_type,
            transaction_ref=transaction.transaction_ref,
            created_by=transaction.created_by,
            updated_by=transaction.updated_by
        )

    def to_domain(self) -> Transaction:
        return Transaction(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            user_id=self.user_id,
            order_id=self.order_id,
            amount=self.amount,
            is_paid=self.is_paid,
            payment_type=self.payment_type,
            transaction_ref=self.transaction_ref,
            created_by=self.created_by,
            updated_by=self.updated_by
        )
