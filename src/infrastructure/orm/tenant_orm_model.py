from sqlalchemy import Column, Integer, String, DateTime, func, Boolean
from domain.models.tenant import Tenant
from infrastructure.db.base_class import Base
from sqlalchemy.dialects.postgresql import JSONB


class TenantOrmModel(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    name = Column(String(96), nullable=False, unique=True, index=True)
    main_contact_name = Column(String(32), nullable=False)
    main_contact_mobile = Column(String(32), nullable=False)
    main_contact_email = Column(String(32), nullable=False)
    main_contact_address = Column(String(64), nullable=False)
    admin = Column(JSONB)
    is_deleted = Column(Boolean, nullable=False, default=False)
    deleted_at = Column(DateTime)
    created_by = Column(Integer, nullable=False, default=0)
    updated_by = Column(Integer, nullable=False, default=0)
    deleted_by = Column(Integer)

    @staticmethod
    def from_domain(tenant: Tenant):
        """Create a TenantOrmModel instance from a Tenant domain model."""
        return TenantOrmModel(
            id=tenant.id,
            created_at=tenant.created_at,
            updated_at=tenant.updated_at,
            name=tenant.name,
            main_contact_name=tenant.main_contact_name,
            main_contact_mobile=tenant.main_contact_mobile,
            main_contact_email=tenant.main_contact_email,
            main_contact_address=tenant.main_contact_address,
            admin=tenant.admin,
            is_deleted=tenant.is_deleted,
            deleted_at=tenant.deleted_at,
            created_by=tenant.created_by,
            updated_by=tenant.updated_by,
            deleted_by=tenant.deleted_by
        )

    def to_domain(self) -> Tenant:
        """Convert this TenantOrmModel instance to a Tenant domain model."""
        return Tenant(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            name=self.name,
            main_contact_name=self.main_contact_name,
            main_contact_mobile=self.main_contact_mobile,
            main_contact_email=self.main_contact_email,
            main_contact_address=self.main_contact_address,
            admin=self.admin,
            is_deleted=self.is_deleted,
            deleted_at=self.deleted_at,
            created_by=self.created_by,
            updated_by=self.updated_by,
            deleted_by=self.deleted_by
        )