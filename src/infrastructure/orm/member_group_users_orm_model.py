from sqlalchemy import Column, Integer, DateTime, func, Boolean, ForeignKey
from domain.models.member_group_users import MemberGroupUsers
from infrastructure.db.base_class import Base


class MemberGroupUsersOrmModel(Base):
    __tablename__ = "member_group_users"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    member_group_id = Column(Integer, ForeignKey('member_groups.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    is_deleted = Column(Boolean, nullable=False, default=False)
    deleted_at = Column(DateTime)
    created_by = Column(Integer, nullable=False, default=0)
    updated_by = Column(Integer, nullable=False, default=0)
    deleted_by = Column(Integer)

    @staticmethod
    def from_domain(member_group_users: MemberGroupUsers):
        """Create a MemberGroupUsersOrmModel instance from a MemberGroupUsers domain model."""
        return MemberGroupUsersOrmModel(
            id=member_group_users.id,
            created_at=member_group_users.created_at,
            updated_at=member_group_users.updated_at,
            member_group_id=member_group_users.member_group_id,
            user_id=member_group_users.user_id,
            is_deleted=member_group_users.is_deleted,
            deleted_at=member_group_users.deleted_at,
            created_by=member_group_users.created_by,
            updated_by=member_group_users.updated_by,
            deleted_by=member_group_users.deleted_by
        )

    def to_domain(self) -> MemberGroupUsers:
        """Convert this MemberGroupUsersOrmModel instance to a MemberGroupUsers domain model."""
        return MemberGroupUsers(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            member_group_id=self.member_group_id,
            user_id=self.user_id,
            is_deleted=self.is_deleted,
            deleted_at=self.deleted_at,
            created_by=self.created_by,
            updated_by=self.updated_by,
            deleted_by=self.deleted_by
        )
