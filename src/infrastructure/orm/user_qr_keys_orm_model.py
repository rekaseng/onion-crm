from sqlalchemy import Column, Integer, String, DateTime, func, Boolean
from domain.models.user_qr_keys import UserQrKeys
from infrastructure.db.base_class import Base


class UserQrKeysOrmModel(Base):
    __tablename__ = "user_qr_keys"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    name = Column(String(64), nullable=False)
    secret = Column(String(128), nullable=False)
    created_by = Column(Integer, nullable=False, default=0)
    updated_by = Column(Integer, nullable=False, default=0)
    deleted_by = Column(Integer)
    is_active = Column(Boolean)

    @staticmethod
    def from_domain(user_qr_keys: UserQrKeys):
        """Create a UserQrKeysOrmModel instance from a UserQrKeys domain model."""
        return UserQrKeysOrmModel(
            id=user_qr_keys.id,
            created_at=user_qr_keys.created_at,
            updated_at=user_qr_keys.updated_at,
            name=user_qr_keys.name,
            secret=user_qr_keys.secret,
            created_by=user_qr_keys.created_by,
            updated_by=user_qr_keys.updated_by,
            deleted_by=user_qr_keys.deleted_by,
            is_active=user_qr_keys.is_active
        )

    def to_domain(self) -> UserQrKeys:
        """Convert this UserQrKeysOrmModel instance to a UserQrKeys domain model."""
        return UserQrKeys(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            name=self.name,
            secret=self.secret,
            created_by=self.created_by,
            updated_by=self.updated_by,
            deleted_by=self.deleted_by,
            is_active=self.is_active
        )