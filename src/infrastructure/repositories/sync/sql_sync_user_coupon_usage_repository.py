from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy.future import select
from fastapi import HTTPException
from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError
from domain.repositories.user_coupon_usage_repository_sync import UserCouponUsageRepositorySync
from domain.models.user_coupon_usage import UserCouponUsage
from infrastructure.orm.user_coupon_usage_orm_model import UserCouponUsageOrmModel

class SQLSyncUserCouponUsageRepository(UserCouponUsageRepositorySync):

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add_sync(self, user_coupon_usage: UserCouponUsage) -> bool:
        orm_user_coupon_usage = UserCouponUsageOrmModel.from_domain(user_coupon_usage)
        try:
            self.db_session.add(orm_user_coupon_usage)
            self.db_session.commit()
            return True
        except SQLAlchemyError as e:
            self.db_session.rollback()
            print(f"SQLAlchemyError: {str(e)}")  # Log the error
            return False


