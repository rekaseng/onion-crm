from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from application.dto.user_dto import MachineLoginDto, MachineLoginWithUserDto, MachineUserCouponDto, \
    MachineUserRewardDto, MachineUserBasicDto
from application.use_cases.user_coupon_use_cases import UserCouponUseCases
from api.deps import get_db, get_current_user, check_permission, get_current_user_auth
from application.use_cases.user_use_cases import UserUseCases
from domain.models.user import UserUpdateDTO
from fastapi import HTTPException
from api.di import get_user_use_cases, get_user_coupon_use_cases, get_reward_point_use_cases
from domain.models.reward_point import RewardPointOption
from infrastructure.helper.substition_cipher import SubstitutionCipher
from application.dto.auth_dto import UserAuthDTO
from application.use_cases.reward_point_use_cases import RewardPointUseCases
from infrastructure.repositories.sql_reward_point_repository import SQLRewardPointRepository
from infrastructure.repositories.sql_payment_method_repository import SQLPaymentMethodRepository
from infrastructure.repositories.sql_store_credit_repository import SQLStoreCreditsRepository
from application.use_cases.payment_method_use_cases import PaymentMethodUseCases
from application.use_cases.store_credit_use_cases import StoreCreditUseCases

router = APIRouter()

@router.get("/qr_code", response_model=dict)
async def get_qr_code(
    current_user: dict = Depends(get_current_user),
    user_use_cases: UserUseCases = Depends(get_user_use_cases)
):
    user_qr_string = await user_use_cases.get_qr_code(current_user)

    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": user_qr_string
    }


@router.post("/machine_login", response_model=dict)
async def machine_login(
    payload: MachineLoginDto,
    current_user: dict = Depends(get_current_user),
    user_use_cases: UserUseCases = Depends(get_user_use_cases),
    db: AsyncSession = Depends(get_db)
):
    user_qr_string = await user_use_cases.get_qr_code(current_user)
    
    payment_method_repository = SQLPaymentMethodRepository(db)
    payment_method_use_cases = PaymentMethodUseCases(payment_method_repository)
    
    store_credits_repository = SQLStoreCreditsRepository(db)
    store_credits_use_cases = StoreCreditUseCases(store_credits_repository)
    
    payment_methods = await payment_method_use_cases.get_by_user_id(current_user["user"].id)
    payment_method = 1 if payment_methods and len(payment_methods) > 0 else 0

    store_credits = await store_credits_use_cases.get_store_credits_balance(current_user["user"].id)
    stored_credits = f"{float(store_credits.balance):.2f}"

    machine_login_with_user_dto = MachineLoginWithUserDto(
        session_ref=payload.session_ref if payload.session_ref else payload.session_id,
        machine_id=payload.machine_id,
        user_id=current_user["user"].id,
        saved_credit_card=payment_method,
        stored_credits=stored_credits,
        user_qr_string=user_qr_string
    )

    print(machine_login_with_user_dto)

    response = await user_use_cases.send_login_to_hq(machine_login_with_user_dto)

    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": response
    }


@router.get("/get_my_coupons", response_model=dict)
async def get_user_coupons(
    user_auth: UserAuthDTO = Depends(get_current_user_auth),
    db: AsyncSession = Depends(get_db),
    user_use_cases: UserUseCases = Depends(get_user_use_cases),
    user_coupon_use_cases: UserCouponUseCases = Depends(get_user_coupon_use_cases),
    reward_point_use_cases: RewardPointUseCases = Depends(get_reward_point_use_cases)
):
    user_id = int(user_auth.user.id)
    user = await user_use_cases.get_by_id(user_id)

    user_dto = MachineUserBasicDto(firstname=user.firstname)

    full_coupons = await user_coupon_use_cases.get_full_coupons_by_user_id(user_id)

    reward_point_options = await reward_point_use_cases.get_user_reward_point_options(user_id)

    coupons_dto = []
    for x in full_coupons:
        coupon_dto = MachineUserCouponDto.from_domain(x)
        coupons_dto.append(coupon_dto)

    machine_user_reward = MachineUserRewardDto(
        user=user_dto,
        coupons = coupons_dto,
        reward_points = reward_point_options
    )
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": machine_user_reward
    }


@router.get("/get_user_coupons/{user_qr_string}", response_model=dict)
async def get_user_coupons(
    user_qr_string: str,
    db: AsyncSession = Depends(get_db),
    user_use_cases: UserUseCases = Depends(get_user_use_cases),
    user_coupon_use_cases: UserCouponUseCases = Depends(get_user_coupon_use_cases),
    reward_point_use_cases: RewardPointUseCases = Depends(get_reward_point_use_cases)

):
    if not user_qr_string.startswith("u-"):
        raise HTTPException(status_code=400, detail="Invalid QR string format")

    encrypted_string = user_qr_string[2:]
    cipher = SubstitutionCipher()
    decrypted_string = cipher.decrypt(encrypted_string)
    user_id_str = decrypted_string.split('-')[0]
    user_id = int(user_id_str)


    user = await user_use_cases.get_by_id(user_id)

    user_dto = MachineUserBasicDto(firstname=user.firstname)

    full_coupons = await user_coupon_use_cases.get_full_coupons_by_user_id(user_id)

    coupons_dto = []
    for x in full_coupons:
        coupon_dto = MachineUserCouponDto.from_domain(x)
        coupons_dto.append(coupon_dto)

    reward_point_options = await reward_point_use_cases.get_user_reward_point_options(user_id)

    machine_user_reward = MachineUserRewardDto(
        user=user_dto,
        coupons = coupons_dto,
        reward_points = reward_point_options
    )

    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": machine_user_reward
    }



@router.get("/get_reward_points", response_model=dict)
async def get_reward_point(
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        db: AsyncSession = Depends(get_db)
):
    reward_point_repository = SQLRewardPointRepository(db)
    reward_point_service = RewardPointUseCases(reward_point_repository)
    coupon = await reward_point_service.get_by_user_id(current_user.user.id)
    return {
         "error_messag.e": None,
         "success": True,
         "error_code": None,
         "result": coupon
    }

@router.get("/get_user_info", response_model=dict)
async def update_user_info(
        user_info: UserUpdateDTO,
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        user_use_cases: UserUseCases = Depends(get_user_use_cases),
        db: AsyncSession = Depends(get_db)
):
    update_user_info = await user_use_cases.update_user_info(current_user.user.id, user_info)

    return {
         "error_message": None,
         "success": True,
         "error_code": None,
         "result": update_user_info
    }

@router.put("/update_user_info", response_model=dict)
async def update_user_info(
        user_info: UserUpdateDTO,
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        user_use_cases: UserUseCases = Depends(get_user_use_cases),
        db: AsyncSession = Depends(get_db)
):
    update_user_info = await user_use_cases.update_user_info(current_user.user.id, user_info)

    return {
         "error_message": None,
         "success": True,
         "error_code": None,
         "result": update_user_info
    }

@router.get("/get_reward_point_balance", response_model=dict)
async def get_reward_point_balance(
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        db: AsyncSession = Depends(get_db)
):
    reward_point_repository = SQLRewardPointRepository(db)
    reward_point_service = RewardPointUseCases(reward_point_repository)
    latest_point = await reward_point_service.get_latest_by_user_id(current_user.user.id)
    balance = latest_point.balance if latest_point else 0
    
    return {
         "error_message": None,
         "success": True,
         "error_code": None,
         "result": balance
    }

