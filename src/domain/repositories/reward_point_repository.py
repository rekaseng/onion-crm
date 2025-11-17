from abc import ABC, abstractmethod
from typing import Optional, List

from domain.models.reward_point import RewardPoint, RewardPointBase


class RewardPointRepository(ABC):
    @abstractmethod
    async def add(self, reward_point: RewardPoint) -> bool:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[RewardPoint]:
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> List[RewardPoint]:
        pass

    @abstractmethod
    async def get_latest_by_user_id(self, user_id: int) -> Optional[RewardPoint]:
        pass

    @abstractmethod
    async def get_by_ids(self, ids: List[int]) -> List[RewardPoint]:
        pass

    @abstractmethod
    async def get_all(self) -> List[RewardPoint]:
        pass

    @abstractmethod
    async def update_reward_point(self, id: int, reward_point_update_dto: RewardPointBase, user_id: int) -> bool:
        pass

    @abstractmethod
    async def delete_reward_point(self, id: int, user_id: int) -> bool:
        pass

