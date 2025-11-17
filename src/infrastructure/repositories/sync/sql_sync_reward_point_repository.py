from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy.future import select
from fastapi import HTTPException
from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError

from domain.repositories.reward_point_repository_sync import RewardPointRepositorySync
from domain.models.reward_point import RewardPoint
from infrastructure.orm.reward_point_orm_model import RewardPointOrmModel

class SQLSyncRewardPointRepository(RewardPointRepositorySync):

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add_sync(self, reward_point: RewardPoint) -> bool:
        orm_model = RewardPointOrmModel.from_domain(reward_point)
        try:
            self.db_session.add(orm_model)
            self.db_session.commit()
            return True
        except SQLAlchemyError as e:
            self.db_session.rollback()
            print(f"SQLAlchemyError: {str(e)}")  # Log the error
            return False
        
    def get_latest_by_user_id_sync(self, user_id: int) -> RewardPoint:
        return self.db_session.query(RewardPointOrmModel).filter(RewardPointOrmModel.user_id == user_id).filter(RewardPointOrmModel.is_deleted == False).order_by(RewardPointOrmModel.id.desc()).limit(1).first()


