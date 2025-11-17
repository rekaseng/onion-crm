from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Boolean
from domain.models.role import Role
from infrastructure.db.base_class import Base
from sqlalchemy.dialects.postgresql import JSONB


class RoleOrmModel(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    name = Column(String(64), unique=True, nullable=False)
    permissions = Column(JSONB)
    tenant_id = Column(Integer, ForeignKey('tenants.id'))
    is_admin = Column(Boolean, nullable=False, default=False)
    is_hq_admin = Column(Boolean, nullable=False, default=False)
    is_deleted = Column(Boolean, nullable=False, default=False)
    deleted_at = Column(DateTime)
    created_by = Column(Integer, nullable=False, default=0)
    updated_by = Column(Integer, nullable=False, default=0)
    deleted_by = Column(Integer)

    @staticmethod
    def from_domain(role: Role):
        """Create a RoleOrmModel instance from a Role domain model."""
        return RoleOrmModel(
            id=role.id,
            created_at=role.created_at,
            updated_at=role.updated_at,
            name=role.name,
            permissions=role.permissions,
            tenant_id=role.tenant_id,
            is_admin=role.is_admin,
            is_hq_admin=role.is_hq_admin,
            is_deleted=role.is_deleted,
            deleted_at=role.deleted_at,
            created_by=role.created_by,
            updated_by=role.updated_by,
            deleted_by=role.deleted_by
        )

    def to_domain(self) -> Role:
        """Convert this RoleOrmModel instance to a Role domain model."""
        return Role(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            name=self.name,
            permissions=self.permissions,
            tenant_id=self.tenant_id,
            is_admin=self.is_admin,
            is_hq_admin=self.is_hq_admin,
            is_deleted=self.is_deleted,
            deleted_at=self.deleted_at,
            created_by=self.created_by,
            updated_by=self.updated_by,
            deleted_by=self.deleted_by
        )