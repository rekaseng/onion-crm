from typing import List

from datetime import datetime

from domain.models.reward_rule import RewardRule, RewardRuleBase
from domain.repositories.reward_rule_repository import RewardRuleRepository

class RewardRuleUseCases:
    def __init__(self, reward_rule_repository: RewardRuleRepository):
        self.reward_rule_repository = reward_rule_repository

    async def add(self, reward_rule_dto: RewardRuleBase, user_id: int) -> bool:
        reward_rule = RewardRule(
            created_at=datetime.now(),
            updated_at=datetime.now(),

            days = reward_rule_dto.days,
            point_modifier = reward_rule_dto.point_modifier,
            
            is_deleted=False,
            deleted_at=None,
            created_by=user_id,
            updated_by=user_id,
            deleted_by=None
        )
        reward_rule = await self.reward_rule_repository.add(reward_rule)
        return reward_rule

    async def get_all(self) -> List[RewardRule]:
        reward_rules = await self.reward_rule_repository.get_all()
        return reward_rules

    async def get_by_id(self, id: int) -> RewardRule:
        reward_rule = await self.reward_rule_repository.get_by_id(id)
        return reward_rule

    async def update_reward_rule(self, id: int, reward_rule_update_dto: RewardRuleBase, user_id: int) -> bool:
        reward_rule = await self.reward_rule_repository.update_reward_rule(id, reward_rule_update_dto, user_id)
        return reward_rule

    async def delete_reward_rule(self, id: int, user_id: int) -> bool:
        reward_rule = await self.reward_rule_repository.delete_reward_rule(id, user_id)
        return reward_rule
