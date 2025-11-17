from sqlalchemy import Column, String, Integer, DateTime, Boolean
from datetime import datetime
from infrastructure.db.base_class import Base
from domain.models.otp import Otp

class OtpOrmModel(Base):
    __tablename__ = 'otps'

    id = Column(Integer, primary_key=True, index=True)
    full_mobile = Column(String, index=True)
    otp = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    attempts = Column(Integer, default=0)

    @staticmethod
    def from_domain(otp: Otp):
        return OtpOrmModel(
            id=otp.id,
            full_mobile=otp.full_mobile,
            otp=otp.otp,
            created_at=otp.created_at,
            attempts=otp.attempts
        )

    def to_domain(self) -> Otp:
        return Otp(
            id=self.id,
            full_mobile=self.full_mobile,
            otp=self.otp,
            created_at=self.created_at,
            attempts=self.attempts
        )
