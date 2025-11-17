from sqlalchemy import Column, Integer, DateTime, func, Boolean, String, Date, ForeignKey
from domain.models.machine_contracts import MachineContracts
from infrastructure.db.base_class import Base


class MachineContractsOrmModel(Base):
    __tablename__ = "machine_contracts"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    start_date = Column(Date, nullable=False, default=False)
    end_date = Column(Date, nullable=False, default=False)
    machine_id = Column(Integer, ForeignKey('machines.id'))
    name = Column(String(128), unique=True, nullable=False)
    tenant_id = Column(Integer, ForeignKey('tenants.id'))
    is_deleted = Column(Boolean, nullable=False, default=False)
    deleted_at = Column(DateTime)
    created_by = Column(Integer, nullable=False, default=0)
    updated_by = Column(Integer, nullable=False, default=0)
    deleted_by = Column(Integer)

    @staticmethod
    def from_domain(machine_contracts: MachineContracts):
        """Create a MachineContractsOrmModel instance from a MachineContracts domain model."""
        return MachineContractsOrmModel(
            id=machine_contracts.id,
            created_at=machine_contracts.created_at,
            updated_at=machine_contracts.updated_at,
            start_date=machine_contracts.start_date,
            end_date=machine_contracts.end_date,
            machine_id=machine_contracts.machine_id,
            name=machine_contracts.name,
            tenant_id=machine_contracts.tenant_id,
            is_deleted=machine_contracts.is_deleted,
            deleted_at=machine_contracts.deleted_at,
            created_by=machine_contracts.created_by,
            updated_by=machine_contracts.updated_by,
            deleted_by=machine_contracts.deleted_by
        )

    def to_domain(self) -> MachineContracts:
        """Convert this MachineContractsOrmModel instance to a MachineContracts domain model."""
        return MachineContracts(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            start_date=self.start_date,
            end_date=self.end_date,
            machine_id=self.machine_id,
            name=self.name,
            tenant_id=self.tenant_id,
            is_deleted=self.is_deleted,
            deleted_at=self.deleted_at,
            created_by=self.created_by,
            updated_by=self.updated_by,
            deleted_by=self.deleted_by
        )
