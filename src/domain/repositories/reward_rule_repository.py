from abc import ABC, abstractmethod
from typing import Optional, List

from domain.models.reward_rule import RewardRule, RewardRuleBase


class RewardRuleRepository(ABC):
    @abstractmethod
    async def add(self, reward_rule: RewardRule) -> bool:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[RewardRule]:
        pass

    @abstractmethod
    async def get_by_ids(self, ids: List[int]) -> List[RewardRule]:
        pass

    @abstractmethod
    async def get_all(self) -> List[RewardRule]:
        pass

    @abstractmethod
    async def update_reward_rule(self, id: int, reward_rule_update_dto: RewardRuleBase, user_id: int) -> bool:
        pass

    @abstractmethod
    async def delete_reward_rule(self, id: int, user_id: int) -> bool:
        pass