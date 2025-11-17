from sqlalchemy import Column, Integer, DECIMAL, DateTime, func, ForeignKey, String, Boolean
from domain.models.store_credit_transaction import StoreCreditTransaction
from domain.models.user_message import UserMessage
from infrastructure.db.base_class import Base


class UserMessageOrmModel(Base):
    __tablename__ = "user_messages"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer)
    user_id = Column(Integer)
    message =  Column(String(400))
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime)
    created_by = Column(Integer)
    updated_by = Column(Integer)

    @staticmethod
    def from_domain(user_message: UserMessage):
        """Create a StoreCreditTransactionOrmModel instance from a StoreCreditTransaction domain model."""
        return UserMessageOrmModel(
            id=user_message.id,
            created_at=user_message.created_at,
            updated_at=user_message.updated_at,
            user_id=user_message.user_id,
            order_id=user_message.order_id,
            message=user_message.message,
            created_by=user_message.created_by,
            updated_by=user_message.updated_by
        )

    def to_domain(self) -> UserMessage:
        """Convert this StoreCreditTransactionOrmModel instance to a StoreCreditTransaction domain model."""
        return UserMessage(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            user_id=self.user_id,
            order_id=self.order_id,
            message=self.message,
            created_by=self.created_by,
            updated_by=self.updated_by
        )
