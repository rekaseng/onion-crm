from sqlalchemy import Column, Integer, func, String, Boolean, DateTime, ForeignKey
from infrastructure.db.base_class import Base
from domain.models.user import User


class UserOrmModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    mobile = Column(String(32), nullable=False, unique=True, index=True)
    country_code = Column(String(32), nullable=False)
    full_mobile = Column(String(32), nullable=False, unique=True, index=True)
    slug = Column(String(96), nullable=False, unique=False, index=True)
    firstname = Column(String(32), nullable=False)
    lastname = Column(String(32), nullable=False)
    email = Column(String(96), nullable=True, index=True)
    birth_year = Column(Integer, default=0)
    birth_month = Column(Integer, default=0)
    birth_day = Column(Integer, default=0)
    password = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    postal_code = Column(String(32), nullable=False)
    email_consent = Column(Boolean)
    sms_consent = Column(Boolean)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    tenant_id = Column(Integer, ForeignKey('tenants.id'))
    is_deleted = Column(Boolean, nullable=False, default=False)
    deleted_at = Column(DateTime)
    created_by = Column(Integer, nullable=False, default=0)
    updated_by = Column(Integer, nullable=False, default=0)
    deleted_by = Column(Integer)

    @staticmethod
    def from_domain(user: User):
        """Create a UserOrmModel instance from a User domain model."""
        return UserOrmModel(
            id=user.id,
            created_at=user.created_at,
            updated_at=user.updated_at,
            mobile=user.mobile,
            country_code=user.country_code,
            full_mobile=user.full_mobile,
            slug=user.slug,
            firstname=user.firstname,
            lastname=user.lastname,
            email=user.email,
            birth_year=user.birth_year,
            birth_month=user.birth_month,
            birth_day=user.birth_day,
            password=user.password,
            address=user.address,
            postal_code=user.postal_code,
            email_consent=user.email_consent,
            sms_consent=user.sms_consent,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            tenant_id=user.tenant_id,
            is_deleted=user.is_deleted,
            deleted_at=user.deleted_at,
            created_by=user.created_by,
            updated_by=user.updated_by,
            deleted_by=user.deleted_by
        )

    def to_domain(self) -> User:
        """Convert this UserOrmModel instance to a User domain model."""
        return User(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            mobile=self.mobile,
            country_code=self.country_code,
            full_mobile=self.full_mobile,
            slug=self.slug,
            firstname=self.firstname,
            lastname=self.lastname,
            email=self.email,
            birth_year=self.birth_year,
            birth_month=self.birth_month,
            birth_day=self.birth_day,
            password=self.password,
            address=self.address,
            postal_code=self.postal_code,
            email_consent=self.email_consent,
            sms_consent=self.sms_consent,
            is_active=self.is_active,
            is_superuser=self.is_superuser,
            tenant_id=self.tenant_id,
            is_deleted=self.is_deleted,
            deleted_at=self.deleted_at,
            created_by=self.created_by,
            updated_by=self.updated_by,
            deleted_by=self.deleted_by
        )
