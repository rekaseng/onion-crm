from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from api.deps import get_db, get_current_user, check_permission, get_current_user_auth
from fastapi import HTTPException
from typing import List
from application.dto.auth_dto import UserAuthDTO
from application.use_cases.reward_rule_use_cases import RewardRuleUseCases
from domain.models.reward_rule import RewardRuleBase
from infrastructure.repositories.sql_reward_rule_repository import SQLRewardRuleRepository

router = APIRouter()


@router.post("/", response_model=dict)
async def reward_rule_add(
        reward_rule_dto: RewardRuleBase,
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        permission: bool = Depends(check_permission("reward_rule_write")),
        db: AsyncSession = Depends(get_db)
):
    reward_rule_repository = SQLRewardRuleRepository(db)
    reward_rule_service = RewardRuleUseCases(reward_rule_repository)
    create_reward_rule_result = await reward_rule_service.add(reward_rule_dto, current_user.user.id)
    if create_reward_rule_result is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong Reward Rule")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": create_reward_rule_result
    }


@router.get("/", response_model=dict)
async def get_reward_rules(
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        permission: bool = Depends(check_permission("reward_rule_read")),
        db: AsyncSession = Depends(get_db)
):
    reward_rule_repository = SQLRewardRuleRepository(db)
    reward_rule_service = RewardRuleUseCases(reward_rule_repository)
    coupons = await reward_rule_service.get_all()
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": {"items": coupons}
    }


@router.get("/{id}", response_model=dict)
async def get_reward_rule(
        id: int,
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        permission: bool = Depends(check_permission("reward_rule_read")),
        db: AsyncSession = Depends(get_db)
):
    reward_rule_repository = SQLRewardRuleRepository(db)
    reward_rule_service = RewardRuleUseCases(reward_rule_repository)
    coupon = await reward_rule_service.get_by_id(id)
    return {
         "error_message": None,
         "success": True,
         "error_code": None,
         "result": coupon
    }


@router.put("/{id}", response_model=dict)
async def reward_rule_update(
        id: int,
        reward_rule_update_dto: RewardRuleBase,
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        permission: bool = Depends(check_permission("reward_rule_write")),
        db: AsyncSession = Depends(get_db)
):
    reward_rule_repository = SQLRewardRuleRepository(db)
    reward_rule_service = RewardRuleUseCases(reward_rule_repository)
    coupon = await reward_rule_service.update_reward_rule(id, reward_rule_update_dto, current_user.user.id)
    if coupon is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Reward Rule Update Unsuccessful")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": []
    }


@router.delete("/{id}", response_model=dict)
async def remove_reward_rule(
        id: int,
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        permission: bool = Depends(check_permission("reward_rule_write")),
        db: AsyncSession = Depends(get_db)
):
    reward_rule_repository = SQLRewardRuleRepository(db)
    reward_rule_service = RewardRuleUseCases(reward_rule_repository)
    coupon = await reward_rule_service.delete_reward_rule(id, current_user.user.id)
    if coupon is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Reward Rule Delete Unsuccessful")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": []
    }
