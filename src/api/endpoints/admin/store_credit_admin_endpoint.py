from datetime import date
from fastapi import APIRouter, Depends, Form, status
from sqlalchemy.ext.asyncio import AsyncSession
from api.deps import get_current_user_auth, get_db, check_permission
from fastapi import HTTPException
from application.dto.auth_dto import UserAuthDTO
from infrastructure.repositories.sql_store_credit_repository import SQLStoreCreditsRepository
from application.use_cases.store_credit_use_cases import StoreCreditUseCases


router = APIRouter()

@router.get("/get_by_user_id/{user_id}", response_model=dict)
async def get_by_user_id(
        user_id: int,
        user_auth: UserAuthDTO = Depends(get_current_user_auth),
        db: AsyncSession = Depends(get_db),
        permission: bool = Depends(check_permission("store_credits_read")),

):
    store_credit_repository = SQLStoreCreditsRepository(db)
    store_credit_service = StoreCreditUseCases(store_credit_repository=store_credit_repository)

    result = await store_credit_service.get_by_user_id(user_id)
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": {"items" :result}
    }