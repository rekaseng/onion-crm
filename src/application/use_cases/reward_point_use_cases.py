from typing import List, Optional

from datetime import datetime

from domain.models.reward_point import RewardPoint, RewardPointBase, RewardPointOption
from domain.repositories.reward_point_repository import RewardPointRepository

class RewardPointUseCases:
    def __init__(self, reward_point_repository: RewardPointRepository):
        self.reward_point_repository = reward_point_repository

    async def add(self, reward_point_dto: RewardPointBase, current_user_id: int) -> bool:
        reward_point = RewardPoint(
            created_at=datetime.now(),
            updated_at=datetime.now(),
            user_id=reward_point_dto.user_id,
            points = reward_point_dto.points,
            order_id = reward_point_dto.order_id,
            type = reward_point_dto.type,
            transaction_at = reward_point_dto.transaction_at,
            description=reward_point_dto.description,
            balance = reward_point_dto.balance,
            is_deleted=False,
            deleted_at=None,
            created_by=current_user_id,
            updated_by=current_user_id,
            deleted_by=None
        )
        reward_point = await self.reward_point_repository.add(reward_point)
        return reward_point

    async def get_all(self) -> List[RewardPoint]:
        reward_points = await self.reward_point_repository.get_all()
        return reward_points

    async def get_by_id(self, id: int) -> RewardPoint:
        reward_point = await self.reward_point_repository.get_by_id(id)
        return reward_point
    
    async def get_by_user_id(self, user_id: int) -> List[RewardPoint]:
        reward_point = await self.reward_point_repository.get_by_user_id(user_id)
        return reward_point

    async def get_user_reward_point_options(self, user_id: int) -> List[RewardPointOption]:
        reward_point = await self.reward_point_repository.get_latest_by_user_id(user_id)
        if not reward_point:
            return []

        reward_point_options = []

        tiers = {
            20: 1.0,
            50: 3.0,
            100: 7.0,
            200: 16.0,
            300: 30.0,
            500: 60.0
        }

        for points, discount in tiers.items():
            if reward_point.balance >= points:
                reward_point_options.append(RewardPointOption(point=points, discount=discount))

        return reward_point_options

    async def update_reward_point(self, id: int, reward_point_update_dto: RewardPointBase, user_id: int) -> bool:
        reward_point = await self.reward_point_repository.update_reward_point(id, reward_point_update_dto, user_id)
        return reward_point

    async def delete_reward_point(self, id: int, user_id: int) -> bool:
        reward_point = await self.reward_point_repository.delete_reward_point(id, user_id)
        return reward_point

    async def get_latest_by_user_id(self, user_id: int) -> Optional[RewardPoint]:
        latest_point = await self.reward_point_repository.get_latest_by_user_id(user_id)
        return latest_point
