from typing import List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from datetime import datetime

from infrastructure.orm.orm_update_helper import update_orm_model_from_domain
from domain.repositories.reward_rule_repository import RewardRuleRepository
from domain.models.reward_rule import RewardRule, RewardRuleBase
from infrastructure.orm.reward_rule_orm_model import RewardRuleOrmModel


class SQLRewardRuleRepository(RewardRuleRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all(self) -> List[RewardRule]:
        result = await self.db_session.execute(select(RewardRuleOrmModel).filter(RewardRuleOrmModel.is_deleted.is_(False)))
        orm_reward_rules = result.scalars().all()
        reward_rules = [item.to_domain() for item in orm_reward_rules]
        return reward_rules

    async def add(self, reward_rule: RewardRule) -> bool:
        reward_rule_result = await self.db_session.execute(select(RewardRuleOrmModel).filter_by(id=reward_rule.id))
        orm_reward_rule = reward_rule_result.scalars().first()

        if orm_reward_rule:
            raise HTTPException(status_code=400, detail="Reward Rule with this id already exists")

        orm_reward_rule = RewardRuleOrmModel.from_domain(reward_rule)
        await self.db_session.merge(orm_reward_rule)
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False

    async def get_by_ids(self, ids: List[int]) -> List[RewardRule]:
        query = select(RewardRuleOrmModel).filter(RewardRuleOrmModel.id.in_(ids), RewardRuleOrmModel.is_deleted.is_(False))
        result = await self.db_session.execute(query)
        orm_reward_rules = result.scalars().all()

        reward_rules = [item.to_domain() for item in orm_reward_rules]

        return reward_rules

    async def get_by_id(self, id: int) -> RewardRule:
        result = await self.db_session.execute(
            select(RewardRuleOrmModel).filter(RewardRuleOrmModel.id == id, RewardRuleOrmModel.is_deleted.is_(False)))
        orm_reward_rule = result.scalars().first()

        if orm_reward_rule is None:
            raise HTTPException(status_code=400, detail="Wrong Reward Rule")

        reward_rule = orm_reward_rule.to_domain()
        return reward_rule

    async def update_reward_rule(self, id:int, update_reward_rule: RewardRuleBase, user_id: int) -> bool:
        reward_rule_result = await self.db_session.execute(
            select(RewardRuleOrmModel).filter(RewardRuleOrmModel.id == id,
                                          RewardRuleOrmModel.is_deleted.is_(False)))
        orm_reward_rule = reward_rule_result.scalars().first()

        if orm_reward_rule is None:
            raise HTTPException(status_code=400, detail="Wrong Reward Rule")
        orm_reward_rule = update_orm_model_from_domain(orm_reward_rule, update_reward_rule)
        orm_reward_rule.updated_at = datetime.now()
        orm_reward_rule.updated_by = user_id
        orm_reward_rule.deleted_by = None
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False

    async def delete_reward_rule(self, id: int, user_id: int) -> bool:
        reward_rule_result = await self.db_session.execute(
            select(RewardRuleOrmModel).filter(RewardRuleOrmModel.id == id, RewardRuleOrmModel.is_deleted.is_(False)))
        orm_reward_rule = reward_rule_result.scalars().first()

        if orm_reward_rule is None:
            raise HTTPException(status_code=400, detail="Wrong Reward Rule")

        orm_reward_rule.updated_at = datetime.now()
        orm_reward_rule.is_deleted = True
        orm_reward_rule.deleted_at = datetime.now()
        orm_reward_rule.updated_by = user_id
        orm_reward_rule.deleted_by = user_id
        try:
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False