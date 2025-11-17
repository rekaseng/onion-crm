from sqlalchemy import Column, Integer, DECIMAL, DateTime, func, ForeignKey, Boolean
from domain.models.store_credits import StoreCredit
from infrastructure.db.base_class import Base


class StoreCreditsOrmModel(Base):
    __tablename__ = "store_credits"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    user_id = Column(Integer, ForeignKey('users.id'))
    balance = Column(DECIMAL(15, 4), nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)
    deleted_at = Column(DateTime)
    created_by = Column(Integer, nullable=False, default=0)
    updated_by = Column(Integer, nullable=False, default=0)
    deleted_by = Column(Integer)

    @staticmethod
    def from_domain(store_credits: StoreCredit):
        """Create a StoreCreditsOrmModel instance from a StoreCredits domain model."""
        return StoreCreditsOrmModel(
            id=store_credits.id,
            created_at=store_credits.created_at,
            updated_at=store_credits.updated_at,
            user_id=store_credits.user_id,
            balance=store_credits.balance,
            is_deleted=store_credits.is_deleted,
            deleted_at=store_credits.deleted_at,
            created_by=store_credits.created_by,
            updated_by=store_credits.updated_by,
            deleted_by=store_credits.deleted_by
        )

    def to_domain(self) -> StoreCredit:
        """Convert this StoreCreditsOrmModel instance to a StoreCredits domain model."""
        return StoreCredit(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            user_id=self.user_id,
            balance=self.balance,
            is_deleted=self.is_deleted,
            deleted_at=self.deleted_at,
            created_by=self.created_by,
            updated_by=self.updated_by,
            deleted_by=self.deleted_by
        )
