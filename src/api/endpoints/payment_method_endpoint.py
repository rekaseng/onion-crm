from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from infrastructure.repositories.sql_payment_method_repository import SQLPaymentMethodRepository
from application.use_cases.payment_method_use_cases import PaymentMethodUseCases
from sqlalchemy.ext.asyncio import AsyncSession
from api.deps import check_permission, get_current_user_auth, get_db
from application.dto.auth_dto import UserAuthDTO

router = APIRouter()

@router.get("/get_my_payment_methods", response_model=dict)
async def get_by_user_id(
        current_user_auth: UserAuthDTO = Depends(get_current_user_auth),
        db: AsyncSession = Depends(get_db)
    ):
    user_id  = current_user_auth.user.id
    payment_method_repository = SQLPaymentMethodRepository(db)
    payment_service = PaymentMethodUseCases(payment_method_repository)
    payment_methods = await payment_service.get_by_user_id(user_id)

    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": payment_methods
    }



@router.delete("", response_model=dict)
async def remove_my_payment_methods(
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        db: AsyncSession = Depends(get_db)
):
    payment_method_repository = SQLPaymentMethodRepository(db)
    payment_service = PaymentMethodUseCases(payment_method_repository)
    result = await payment_service.delete_payment_method(current_user.user.id)
    if result is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Payment Method Delete Unsuccessful")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": []
    }