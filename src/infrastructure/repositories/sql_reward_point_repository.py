from typing import List, Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from datetime import datetime

from infrastructure.orm.orm_update_helper import update_orm_model_from_domain
from domain.repositories.reward_point_repository import RewardPointRepository
from domain.models.reward_point import RewardPoint, RewardPointBase
from infrastructure.orm.reward_point_orm_model import RewardPointOrmModel


class SQLRewardPointRepository(RewardPointRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all(self) -> List[RewardPoint]:
        result = await self.db_session.execute(select(RewardPointOrmModel).filter(RewardPointOrmModel.is_deleted.is_(False)))
        orm_reward_points = result.scalars().all()
        reward_points = [item.to_domain() for item in orm_reward_points]
        return reward_points

    async def add(self, reward_point: RewardPoint) -> bool:
        reward_point_result = await self.db_session.execute(select(RewardPointOrmModel).filter_by(id=reward_point.id))
        orm_reward_point = reward_point_result.scalars().first()

        if orm_reward_point:
            raise HTTPException(status_code=400, detail="Reward Point with this id already exists")

        orm_reward_point = RewardPointOrmModel.from_domain(reward_point)
        await self.db_session.merge(orm_reward_point)
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False

    async def get_by_ids(self, ids: List[int]) -> List[RewardPoint]:
        query = select(RewardPointOrmModel).filter(RewardPointOrmModel.id.in_(ids), RewardPointOrmModel.is_deleted.is_(False))
        result = await self.db_session.execute(query)
        orm_reward_points = result.scalars().all()

        reward_points = [item.to_domain() for item in orm_reward_points]

        return reward_points
    
    async def get_by_user_id(self, user_id: int) -> List[RewardPoint]:
        query = select(RewardPointOrmModel).filter(RewardPointOrmModel.user_id == user_id, RewardPointOrmModel.is_deleted.is_(False))
        result = await self.db_session.execute(query)
        orm_reward_points = result.scalars().all()

        reward_points = [item.to_domain() for item in orm_reward_points]

        return reward_points

    async def get_latest_by_user_id(self, user_id: int) -> Optional[RewardPoint]:
        query = (
            select(RewardPointOrmModel).
            filter(RewardPointOrmModel.user_id == user_id, RewardPointOrmModel.is_deleted.is_(False))
            .order_by(RewardPointOrmModel.id.desc())
            .limit(1)
        )
        reward_point = None
        result = await self.db_session.execute(query)
        orm_reward_point = result.scalars().first()
        if orm_reward_point:
            reward_point = orm_reward_point.to_domain()

        return reward_point

    async def get_by_id(self, id: int) -> RewardPoint:
        result = await self.db_session.execute(
            select(RewardPointOrmModel).filter(RewardPointOrmModel.id == id, RewardPointOrmModel.is_deleted.is_(False)))
        orm_reward_point = result.scalars().first()

        if orm_reward_point is None:
            raise HTTPException(status_code=400, detail="Wrong Reward Point")

        reward_point = orm_reward_point.to_domain()
        return reward_point

    async def update_reward_point(self, id:int, update_reward_point: RewardPointBase, user_id: int) -> bool:
        reward_point_result = await self.db_session.execute(
            select(RewardPointOrmModel).filter(RewardPointOrmModel.id == id,
                                          RewardPointOrmModel.is_deleted.is_(False)))
        orm_reward_point = reward_point_result.scalars().first()

        if orm_reward_point is None:
            raise HTTPException(status_code=400, detail="Wrong Reward Point")
        orm_reward_point = update_orm_model_from_domain(orm_reward_point, update_reward_point)
        orm_reward_point.updated_at = datetime.now()
        orm_reward_point.updated_by = user_id
        orm_reward_point.deleted_by = None
        orm_reward_point.transaction_at = update_reward_point.transaction_at.replace(tzinfo=None)
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False

    async def delete_reward_point(self, id: int, user_id: int) -> bool:
        reward_point_result = await self.db_session.execute(
            select(RewardPointOrmModel).filter(RewardPointOrmModel.id == id, RewardPointOrmModel.is_deleted.is_(False)))
        orm_reward_point = reward_point_result.scalars().first()

        if orm_reward_point is None:
            raise HTTPException(status_code=400, detail="Wrong Reward Point")

        orm_reward_point.updated_at = datetime.now()
        orm_reward_point.is_deleted = True
        orm_reward_point.deleted_at = datetime.now()
        orm_reward_point.updated_by = user_id
        orm_reward_point.deleted_by = user_id
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False