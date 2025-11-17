from datetime import date
from fastapi import APIRouter, Depends, Form, status
from sqlalchemy.ext.asyncio import AsyncSession
from api.deps import get_current_user_auth, get_db, check_permission
from fastapi import HTTPException
from application.use_cases.payment_use_cases import PaymentUseCases
from domain.models.two_c_two_p_payments import TwoCTwoPRequestPaymentRequest, TwoCTwoPDirectPaymentRequest
from domain.models.payment import PaymentBase
from infrastructure.repositories.sql_payment_repository import SQLPaymentRepository
from application.use_cases.payment_method_use_cases import PaymentMethodUseCases
from infrastructure.repositories.sql_payment_method_repository import SQLPaymentMethodRepository
from application.dto.auth_dto import UserAuthDTO


router = APIRouter()

@router.post("/request_direct_payment", response_model=dict)
async def request_direct_payment(
        payload: TwoCTwoPDirectPaymentRequest,
        user_auth: UserAuthDTO = Depends(get_current_user_auth),
        db: AsyncSession = Depends(get_db),
        permission: bool = Depends(check_permission("user_write")),

):
    payment_repository = SQLPaymentRepository(db)
    payment_service = PaymentUseCases(payment_repository=payment_repository)
    payment_method_repository = SQLPaymentMethodRepository(db)
    payment_method_service = PaymentMethodUseCases(payment_method_repository=payment_method_repository)
    payment_methods = await payment_method_service.get_by_user_id(payload.customer_id)
    customer_tokens = [item.payment_token for item in payment_methods]

    if customer_tokens.__len__() == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Cannot pay because don't have customer token")

    payment_dto = PaymentBase(
        amount=payload.amount,
        invoice_no=payload.invoiceNo,
        success=False
    )
    new_payment = await payment_service.add(payment_dto, user_auth.user.id)
    if new_payment is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong Payment")

    payment_token_response = await payment_service.request_payment(amount=payload.amount, name=payload.name,
                                                                   desc=payload.description,
                                                                   invoiceNo=payload.invoiceNo,
                                                                   customerToken=customer_tokens)
    if payment_token_response is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong Request Payment")

    payment_token = payment_token_response.paymentToken
    payment_response = await payment_service.request_card_payment(paymentToken=payment_token, customerToken=customer_tokens)
    if payment_response is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong Direct Payment")

    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": payment_response.__dict__
    }


@router.get("/history", response_model=dict)
async def get_payment_history(
        start_date: date,
        end_date: date,
        user_auth: UserAuthDTO = Depends(get_current_user_auth),
        db: AsyncSession = Depends(get_db),
        permission: bool = Depends(check_permission("payment_read")),

):
    payment_repository = SQLPaymentRepository(db)
    payment_service = PaymentUseCases(payment_repository=payment_repository)

    result = await payment_service.get_by_date_range(start_date, end_date)
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": {"items" :result}
    }

@router.get("/get_by_user_id/{user_id}", response_model=dict)
async def get_payment_by_user_id(
        user_id: int,
        user_auth: UserAuthDTO = Depends(get_current_user_auth),
        db: AsyncSession = Depends(get_db),
        permission: bool = Depends(check_permission("payment_read")),

):
    payment_repository = SQLPaymentRepository(db)
    payment_service = PaymentUseCases(payment_repository=payment_repository)

    result = await payment_service.get_by_user_id(user_id)
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": {"items" :result}
    }


@router.get("/{id}", response_model=dict)
async def get_payment_by_id(
        id: int,
        user_auth: UserAuthDTO = Depends(get_current_user_auth),
        db: AsyncSession = Depends(get_db),
        permission: bool = Depends(check_permission("payment_read")),

):
    payment_repository = SQLPaymentRepository(db)
    payment_service = PaymentUseCases(payment_repository=payment_repository)

    result = await payment_service.get_by_id(id)
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": result.__dict__
    }

