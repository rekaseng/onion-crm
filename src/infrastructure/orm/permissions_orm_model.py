from sqlalchemy import Column, Integer, String, DateTime, Boolean
from domain.models.permission import Permission
from infrastructure.db.base_class import Base


class PermissionOrmModel(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True)
    name = Column(String(96), nullable=False, unique=True, index=True)
    is_deleted = Column(Boolean, nullable=False, default=False)
    deleted_at = Column(DateTime)
    created_by = Column(Integer, nullable=False, default=0)
    updated_by = Column(Integer, nullable=False, default=0)
    deleted_by = Column(Integer)

    @staticmethod
    def from_domain(permission: Permission):
        """Create a PermissionOrmModel instance from a Permission domain model."""
        return PermissionOrmModel(
            id=permission.id,
            name=permission.name,
            is_deleted=permission.is_deleted,
            deleted_at=permission.deleted_at,
            created_by=permission.created_by,
            updated_by=permission.updated_by,
            deleted_by=permission.deleted_by
        )

    def to_domain(self) -> Permission:
        """Convert this PermissionOrmModel instance to a Permission domain model."""
        return Permission(
            id=self.id,
            name=self.name,
            is_deleted=self.is_deleted,
            deleted_at=self.deleted_at,
            created_by=self.created_by,
            updated_by=self.updated_by,
            deleted_by=self.deleted_by
        )
