from sqlalchemy import Column, Integer, func, DateTime, ForeignKey, Boolean
from infrastructure.db.base_class import Base
from domain.models.user_role import UserRole


class UserRoleOrmModel(Base):
    __tablename__ = "user_roles"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    user_id = Column(Integer, ForeignKey('users.id'))
    role_id = Column(Integer, ForeignKey('roles.id'))
    is_deleted = Column(Boolean, nullable=False, default=False)
    deleted_at = Column(DateTime)
    created_by = Column(Integer, nullable=False, default=0)
    updated_by = Column(Integer, nullable=False, default=0)
    deleted_by = Column(Integer)

    @staticmethod
    def from_domain(user_role: UserRole):
        """Create a UserOrmModel instance from a User domain model."""
        return UserRoleOrmModel(
            id=user_role.id,
            created_at=user_role.created_at,
            updated_at=user_role.updated_at,
            user_id=user_role.user_id,
            role_id=user_role.role_id,
            is_deleted=user_role.is_deleted,
            deleted_at=user_role.deleted_at,
            created_by=user_role.created_by,
            updated_by=user_role.updated_by,
            deleted_by=user_role.deleted_by
        )

    def to_domain(self) -> UserRole:
        """Convert this UserOrmModel instance to a User domain model."""
        return UserRole(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            user_id=self.user_id,
            role_id=self.role_id,
            is_deleted=self.is_deleted,
            deleted_at=self.deleted_at,
            created_by=self.created_by,
            updated_by=self.updated_by,
            deleted_by=self.deleted_by
        )