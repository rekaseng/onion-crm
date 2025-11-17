from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from application.dto.auth_dto import UserAuthDTO
from application.dto.order_dto import OrderDeductAmountDto, OrderSendMessageDto
from application.dto.user_dto import UserAdjustWalletDto
from application.use_cases.payment_use_cases import PaymentUseCases
from application.use_cases.store_credit_use_cases import StoreCreditUseCases
from domain.models.store_credit_transaction import StoreCreditTransactionType
from domain.models.user import UserBase
from api.deps import get_db, get_current_user, check_permission, get_hq_admin, get_current_user_auth, get_admin
from application.use_cases.user_use_cases import UserUseCases
from application.use_cases.communication_use_cases import CommunicationUseCases
from api.di import get_user_use_cases, get_payment_use_cases, get_store_credit_use_cases, get_communication_use_cases
from fastapi import HTTPException
from application.use_cases.reward_point_use_cases import RewardPointUseCases
from infrastructure.repositories.sql_reward_point_repository import SQLRewardPointRepository

router = APIRouter()

@router.post("/", response_model=dict)
async def add_user_admin(
    user_admin_dto: UserBase,
    current_user: dict = Depends(get_current_user),
    permission: bool = Depends(check_permission("user_write")),
    is_hq_admin: bool = Depends(get_hq_admin),
    user_use_cases: UserUseCases = Depends(get_user_use_cases)  # Inject UserUseCases with all dependencies
):
    new_user_admin = await user_use_cases.add_user_admin(user_admin_dto)
    if new_user_admin is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong User Admin")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": [new_user_admin]
    }


@router.post("/", response_model=dict)
async def add_user(
    user_dto: UserBase,
    user_use_cases: UserUseCases = Depends(get_user_use_cases)
):
    new_user = await user_use_cases.add_user(user_dto)
    if new_user is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong User")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": new_user
    }

@router.get("/", response_model=dict)
async def get_users(
    current_user: dict = Depends(get_current_user),
    permission: bool = Depends(check_permission("user_read")),
    user_use_cases: UserUseCases = Depends(get_user_use_cases)
):
    users = await user_use_cases.get_all(current_user)
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": {"items": users}
    }


@router.get("/{id}", response_model=dict)
async def get_user(
    id: int,
    current_user: dict = Depends(get_current_user),
    permission: bool = Depends(check_permission("user_read")),
    user_use_cases: UserUseCases = Depends(get_user_use_cases)
):
    user = await user_use_cases.get_by_id(id)
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": user
    }


@router.post("/send_sms", response_model=dict)
async def send_sms(
        obj_in: OrderSendMessageDto,
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        permission: bool = Depends(check_permission("orders_read")),
        is_admin: bool = Depends(get_admin),
        db: AsyncSession = Depends(get_db),
        communication_use_cases: CommunicationUseCases = Depends(get_communication_use_cases),
        user_use_cases: UserUseCases = Depends(get_user_use_cases)
):
    user = await user_use_cases.get_by_id(obj_in.customer_id)
    result = await communication_use_cases.send_message(user.full_mobile, obj_in.message)
    

    # Save the message in user_message db
    await user_use_cases.save_message(
        user_id=obj_in.customer_id,
        order_id=None,
        message=obj_in.message,
        admin_id=current_user.user.id
    )

    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": result
    }

@router.post("/adjust_wallet", response_model=dict)
async def adjust_wallet(
    obj_in: OrderDeductAmountDto,
    current_user: UserAuthDTO = Depends(get_current_user_auth),
    permission: bool = Depends(check_permission("user_read")),
    user_use_cases: UserUseCases = Depends(get_user_use_cases),
    store_credit_service: StoreCreditUseCases = Depends(get_store_credit_use_cases)
):
    store_credit_type = StoreCreditTransactionType.CREDIT
    if(obj_in.amount < 0 ):
        obj_in.amount = obj_in.amount * -1
        store_credit_type = StoreCreditTransactionType.DEBIT

    result = await store_credit_service.manual_order_wallet_adjustment(
        current_user.user.id,
        obj_in,
        store_credit_type
    )

    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": result
    }

@router.put("/{id}", response_model=dict)
async def change_userinfo(
    id: int,
    user_update_dto: UserBase,
    current_user: dict = Depends(get_current_user),
    permission: bool = Depends(check_permission("user_write")),
    user_use_cases: UserUseCases = Depends(get_user_use_cases)
):
    user = await user_use_cases.update_user_info(id, user_update_dto, current_user)
    if user is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User Update Unsuccessful")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": []
    }

@router.delete("/{user_id}", response_model=dict)
async def remove_user(
    user_id: int,
    current_user: dict = Depends(get_current_user),
    permission: bool = Depends(check_permission("user_write")),
    user_use_cases: UserUseCases = Depends(get_user_use_cases)
):
    user = await user_use_cases.delete_user(user_id, current_user)
    if user is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User Delete Unsuccessful")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": []
    }

@router.get("/get_messages/{user_id}", response_model=dict)
async def get_user_messages(
    user_id: int,
    current_user: UserAuthDTO = Depends(get_current_user_auth),
    permission: bool = Depends(check_permission("user_read")),
    is_admin: bool = Depends(get_admin),
    user_use_cases: UserUseCases = Depends(get_user_use_cases)
):
    messages = await user_use_cases.get_user_messages(user_id)
    if messages is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No messages found")


    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": {"items": messages}
    }

@router.get("/get_reward_point_balance/{user_id}", response_model=dict)
async def get_reward_point_balance(
        user_id: int,
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        permission: bool = Depends(check_permission("user_read")),
        db: AsyncSession = Depends(get_db)
):
    reward_point_repository = SQLRewardPointRepository(db)
    reward_point_service = RewardPointUseCases(reward_point_repository)
    latest_point = await reward_point_service.get_latest_by_user_id(user_id)
    balance = latest_point.balance if latest_point else 0
    
    return {
         "error_message": None,
         "success": True,
         "error_code": None,
         "result": balance
    }

@router.get("/get_reward_points_by_user/{user_id}", response_model=dict)
async def get_reward_points_by_user(
        user_id: int,
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        permission: bool = Depends(check_permission("user_read")),
        db: AsyncSession = Depends(get_db)
):
    reward_point_repository = SQLRewardPointRepository(db)
    reward_point_service = RewardPointUseCases(reward_point_repository)
    reward_point = await reward_point_service.get_by_user_id(user_id)

    
    return {
         "error_message": None,
         "success": True,
         "error_code": None,
         "result": reward_point
    }