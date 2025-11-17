from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from api.deps import get_db, get_current_user, check_permission, get_current_user_auth
from fastapi import HTTPException
from typing import List
from application.dto.auth_dto import UserAuthDTO
from application.use_cases.reward_point_use_cases import RewardPointUseCases
from domain.models.reward_point import RewardPointBase
from infrastructure.repositories.sql_reward_point_repository import SQLRewardPointRepository

router = APIRouter()


@router.post("/", response_model=dict)
async def reward_point_add(
        reward_point_dto: RewardPointBase,
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        permission: bool = Depends(check_permission("reward_point_write")),
        db: AsyncSession = Depends(get_db)
):
    reward_point_repository = SQLRewardPointRepository(db)
    reward_point_service = RewardPointUseCases(reward_point_repository)
    create_reward_point_status = await reward_point_service.add(reward_point_dto, current_user.user.id)
    if create_reward_point_status is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong Reward Point")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": create_reward_point_status
    }


@router.get("/", response_model=dict)
async def get_reward_points(
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        permission: bool = Depends(check_permission("reward_point_read")),
        db: AsyncSession = Depends(get_db)
):
    reward_point_repository = SQLRewardPointRepository(db)
    reward_point_service = RewardPointUseCases(reward_point_repository)
    coupons = await reward_point_service.get_all()
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": {"items": coupons}
    }


@router.get("/get_reward_point_by_user/{user_id}", response_model=dict)
async def get_reward_point(
        user_id: int,
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        permission: bool = Depends(check_permission("reward_point_read")),
        db: AsyncSession = Depends(get_db)
):
    reward_point_repository = SQLRewardPointRepository(db)
    reward_point_service = RewardPointUseCases(reward_point_repository)
    coupon = await reward_point_service.get_by_user_id(user_id)
    return {
         "error_message": None,
         "success": True,
         "error_code": None,
         "result": coupon
    }


@router.get("/{id}", response_model=dict)
async def get_reward_point(
        id: int,
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        permission: bool = Depends(check_permission("reward_point_read")),
        db: AsyncSession = Depends(get_db)
):
    reward_point_repository = SQLRewardPointRepository(db)
    reward_point_service = RewardPointUseCases(reward_point_repository)
    coupon = await reward_point_service.get_by_id(id)
    return {
         "error_message": None,
         "success": True,
         "error_code": None,
         "result": coupon
    }


@router.put("/{id}", response_model=dict)
async def reward_point_update(
        id: int,
        reward_point_update_dto: RewardPointBase,
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        permission: bool = Depends(check_permission("reward_point_write")),
        db: AsyncSession = Depends(get_db)
):
    reward_point_repository = SQLRewardPointRepository(db)
    reward_point_service = RewardPointUseCases(reward_point_repository)
    coupon = await reward_point_service.update_reward_point(id, reward_point_update_dto, current_user.user.id)
    if coupon is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Reward Point Update Unsuccessful")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": []
    }


@router.delete("/{id}", response_model=dict)
async def remove_reward_point(
        id: int,
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        permission: bool = Depends(check_permission("reward_point_write")),
        db: AsyncSession = Depends(get_db)
):
    reward_point_repository = SQLRewardPointRepository(db)
    reward_point_service = RewardPointUseCases(reward_point_repository)
    coupon = await reward_point_service.delete_reward_point(id, current_user.user.id)
    if coupon is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Reward Point Delete Unsuccessful")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": []
    }
