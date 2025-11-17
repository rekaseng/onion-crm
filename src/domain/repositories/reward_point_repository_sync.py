from abc import ABC, abstractmethod
from typing import Optional, List

from domain.models.reward_point import RewardPoint, RewardPointBase


class RewardPointRepositorySync(ABC):
    @abstractmethod
    def add_sync(self, reward_point: RewardPoint) -> bool:
        pass

    @abstractmethod
    def get_latest_by_user_id_sync(self, user_id: int) -> RewardPoint:
        pass