from sqlalchemy import Column, Integer, String, DateTime, Boolean, func
from infrastructure.db.base_class import Base
from domain.models.sku import Sku

class SkuOrmModel(Base):
    __tablename__ = "skus"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(),
                        onupdate=func.current_timestamp())
    name = Column(String(128), nullable=False)
    sku = Column(String(128), nullable=False)
    source_id = Column(Integer)
    is_deleted = Column(Boolean, nullable=False, default=False)
    deleted_at = Column(DateTime)
    created_by = Column(Integer, nullable=False, default=0)
    updated_by = Column(Integer, nullable=False, default=0)
    deleted_by = Column(Integer)

    @staticmethod
    def from_domain(sku: Sku):
        """Create a SkuOrmModel instance from a product domain model."""
        return SkuOrmModel(
            id=sku.id,
            created_at=sku.created_at,
            updated_at=sku.updated_at,
            name=sku.name,
            sku=sku.sku,
            is_deleted=sku.is_deleted,
            deleted_at=sku.deleted_at,
            created_by=sku.created_by,
            updated_by=sku.updated_by,
            deleted_by=sku.deleted_by
        )

    def to_domain(self) -> Sku:
        """Convert this SkuOrmModel instance to a Sku domain model."""
        return Sku(
            id=self.id,
            source_id=self.source_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            name=self.name,
            sku=self.sku,
            is_deleted=self.is_deleted,
            deleted_at=self.deleted_at,
            created_by=self.created_by,
            updated_by=self.updated_by,
            deleted_by=self.deleted_by
        )


