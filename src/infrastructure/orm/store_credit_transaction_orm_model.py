from sqlalchemy import Column, Integer, DECIMAL, DateTime, func, ForeignKey, String, Boolean
from domain.models.store_credit_transaction import StoreCreditTransaction
from infrastructure.db.base_class import Base


class StoreCreditTransactionOrmModel(Base):
    __tablename__ = "store_credit_transaction"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    order_id = Column(Integer, index=True)
    description=Column(String(400))
    type = Column(String(32), nullable=False)
    store_credit_id = Column(Integer, ForeignKey('store_credits.id'))
    amount = Column(DECIMAL(15, 4), nullable=False)

    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    is_deleted = Column(Boolean, nullable=False, default=False)
    deleted_at = Column(DateTime)
    created_by = Column(Integer, nullable=False, default=0)
    updated_by = Column(Integer, nullable=False, default=0)
    deleted_by = Column(Integer)

    @staticmethod
    def from_domain(store_credit_transaction: StoreCreditTransaction):
        """Create a StoreCreditTransactionOrmModel instance from a StoreCreditTransaction domain model."""
        return StoreCreditTransactionOrmModel(
            id=store_credit_transaction.id,
            user_id=store_credit_transaction.user_id,
            order_id=store_credit_transaction.order_id,
            created_at=store_credit_transaction.created_at,
            updated_at=store_credit_transaction.updated_at,
            type=store_credit_transaction.type,
            description=store_credit_transaction.description,
            store_credit_id=store_credit_transaction.store_credit_id,
            amount=store_credit_transaction.amount,
            is_deleted=store_credit_transaction.is_deleted,
            deleted_at=store_credit_transaction.deleted_at,
            created_by=store_credit_transaction.created_by,
            updated_by=store_credit_transaction.updated_by,
            deleted_by=store_credit_transaction.deleted_by
        )

    def to_domain(self) -> StoreCreditTransaction:
        """Convert this StoreCreditTransactionOrmModel instance to a StoreCreditTransaction domain model."""
        return StoreCreditTransaction(
            id=self.id,
            user_id=self.user_id,
            order_id=self.order_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            type=self.type,
            description=self.description,
            store_credit_id=self.store_credit_id,
            amount=self.amount,
            is_deleted=self.is_deleted,
            deleted_at=self.deleted_at,
            created_by=self.created_by,
            updated_by=self.updated_by,
            deleted_by=self.deleted_by
        )
