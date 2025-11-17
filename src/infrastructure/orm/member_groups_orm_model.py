from sqlalchemy import Column, Integer, DateTime, func, Boolean, String, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB

from domain.models.member_groups import MemberGroup
from infrastructure.db.base_class import Base


class MemberGroupOrmModel(Base):
    __tablename__ = "member_groups"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    is_active = Column(Boolean, nullable=False, default=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1000))
    user_ids = Column(JSONB)
    all_users = Column(Boolean, default=False)
    slug = Column(String(128), nullable=False, unique=True, index=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'))
    is_global = Column(Boolean, default=False)
    is_deleted = Column(Boolean, nullable=False, default=False)
    deleted_at = Column(DateTime)
    created_by = Column(Integer, nullable=False, default=0)
    updated_by = Column(Integer, nullable=False, default=0)
    deleted_by = Column(Integer)

    @staticmethod
    def from_domain(domain: MemberGroup):
        """Create a MemberGroupsOrmModel instance from a MemberGroups domain model."""
        return MemberGroupOrmModel(
            id=domain.id,
            created_at=domain.created_at,
            updated_at=domain.updated_at,
            is_active=domain.is_active,
            name=domain.name,
            description=domain.description,
            all_users=domain.all_users,
            user_ids=domain.user_ids,
            slug=domain.slug,
            tenant_id=domain.tenant_id,
            is_global=domain.is_global,
            is_deleted=domain.is_deleted,
            deleted_at=domain.deleted_at,
            created_by=domain.created_by,
            updated_by=domain.updated_by,
            deleted_by=domain.deleted_by
        )

    def to_domain(self) -> MemberGroup:
        """Convert this MemberGroupsOrmModel instance to a MemberGroups domain model."""
        return MemberGroup(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            is_active=self.is_active,
            name=self.name,
            all_users=self.all_users,
            description=self.description,
            user_ids=self.user_ids,
            slug=self.slug,
            tenant_id=self.tenant_id,
            is_global=self.is_global,
            is_deleted=self.is_deleted,
            deleted_at=self.deleted_at,
            created_by=self.created_by,
            updated_by=self.updated_by,
            deleted_by=self.deleted_by
        )
