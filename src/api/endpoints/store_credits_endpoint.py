from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from api.deps import get_db, get_current_user, check_permission, get_current_user_auth
from api.di import get_store_credit_use_cases
from application.use_cases.store_credit_use_cases import StoreCreditUseCases
from infrastructure.repositories.sql_store_credit_repository import SQLStoreCreditsRepository
from db_error_handlers import handle_db_errors

from application.dto.auth_dto import UserAuthDTO

router = APIRouter()


@router.get("/", response_model=dict)
async def get_all_store_credits(
        current_user: dict = Depends(get_current_user),
        permission: bool = Depends(check_permission("store_credits_read")),
        db: AsyncSession = Depends(get_db),
        store_credit_service: StoreCreditUseCases =  Depends(get_store_credit_use_cases)
):
    store_credits = await store_credit_service.get_all(current_user)
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": {"items" : store_credits}
    }


@router.get("/balance", response_model=dict)
@handle_db_errors
async def get_store_credits_balance(
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        db: AsyncSession = Depends(get_db),
        store_credit_service: StoreCreditUseCases = Depends(get_store_credit_use_cases)

):
    store_credit = await store_credit_service.get_store_credits_balance(current_user.user.id)
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": {
            "user_id": store_credit.user_id,
            "store_credit_id": store_credit.id,
            "balance": store_credit.balance
        }
    }


@router.get("/balance/{user_id}", response_model=dict) #deprecated
@handle_db_errors
async def get_store_credits_balance(
        user_id: int,
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        permission: bool = Depends(check_permission("store_credits_read")),
        db: AsyncSession = Depends(get_db)
):
    store_credits_repository = SQLStoreCreditsRepository(db)
    store_credits_service = StoreCreditUseCases(store_credits_repository)
    store_credits = await store_credits_service.get_store_credits_balance(user_id)
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": {
            "user_id": store_credits.user_id,
            "store_credit_id": store_credits.id,
            "balance": store_credits.balance
        }
    }