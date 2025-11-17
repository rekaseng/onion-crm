from sqlalchemy import Column, Integer, DateTime, func, Boolean, String
from domain.models.machines import Machines
from infrastructure.db.base_class import Base


class MachinesOrmModel(Base):
    __tablename__ = "machines"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    is_active = Column(Boolean, nullable=False, default=False)
    name = Column(String(128), unique=True, nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)
    deleted_at = Column(DateTime)
    created_by = Column(Integer, nullable=False, default=0)
    updated_by = Column(Integer, nullable=False, default=0)
    deleted_by = Column(Integer)

    @staticmethod
    def from_domain(machines: Machines):
        """Create a MachinesOrmModel instance from a Machines domain model."""
        return MachinesOrmModel(
            id=machines.id,
            created_at=machines.created_at,
            updated_at=machines.updated_at,
            is_active=machines.is_active,
            name=machines.name,
            is_deleted=machines.is_deleted,
            deleted_at=machines.deleted_at,
            created_by=machines.created_by,
            updated_by=machines.updated_by,
            deleted_by=machines.deleted_by
        )

    def to_domain(self) -> Machines:
        """Convert this MachinesOrmModel instance to a Machines domain model."""
        return Machines(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            is_active=self.is_active,
            name=self.name,
            is_deleted=self.is_deleted,
            deleted_at=self.deleted_at,
            created_by=self.created_by,
            updated_by=self.updated_by,
            deleted_by=self.deleted_by
        )
