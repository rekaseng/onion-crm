from sqlalchemy import Column, Integer, String, DateTime, Boolean, func, ForeignKey
from domain.models.refresh_token import RefreshToken
from infrastructure.db.base_class import Base


class RefreshTokenOrmModel(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    user_id = Column(Integer, ForeignKey('users.id'))
    refresh_token = Column(String(64), nullable=False)
    invalidate = Column(Boolean, nullable=False)
    expiry = Column(DateTime, nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)
    deleted_at = Column(DateTime)
    created_by = Column(Integer, nullable=False, default=0)
    updated_by = Column(Integer, nullable=False, default=0)
    deleted_by = Column(Integer)

    @staticmethod
    def from_domain(refresh_token: RefreshToken):
        """Create a RefreshTokenOrmModel instance from a RefreshToken domain model."""
        return RefreshTokenOrmModel(
            id=refresh_token.id,
            created_at=refresh_token.created_at,
            updated_at=refresh_token.updated_at,
            user_id=refresh_token.user_id,
            refresh_token=refresh_token.refresh_token,
            invalidate=refresh_token.invalidate,
            expiry=refresh_token.expiry,
            is_deleted=refresh_token.is_deleted,
            deleted_at=refresh_token.deleted_at,
            created_by=refresh_token.created_by,
            updated_by=refresh_token.updated_by,
            deleted_by=refresh_token.deleted_by
        )

    def to_domain(self) -> RefreshToken:
        """Convert this RefreshTokenOrmModel instance to a RefreshToken domain model."""
        return RefreshToken(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            user_id=self.user_id,
            refresh_token=self.refresh_token,
            invalidate=self.invalidate,
            expiry=self.expiry,
            is_deleted=self.is_deleted,
            deleted_at=self.deleted_at,
            created_by=self.created_by,
            updated_by=self.updated_by,
            deleted_by=self.deleted_by
        )
