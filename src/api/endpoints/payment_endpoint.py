from datetime import datetime
from fastapi import APIRouter, Depends, Form, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from api.deps import get_current_user_auth, get_db
from fastapi import HTTPException

from api.di import get_payment_use_cases
from domain.models.paynow import Paynow
from application.use_cases.payment_use_cases import PaymentUseCases
from domain.models.two_c_two_p_payments import TwoCTwoPPaymentWebHookRequest, TwoCTwoPRequestPaymentRequest
from utils.constants import PAYMENT_TYPE_CREDIT_CARD
from utils.security import decode_payment_result_token
from domain.models.payment import PaymentBase
from application.use_cases.payment_method_use_cases import PaymentMethodUseCases
from domain.models.payment_method import PaymentMethodBase
from infrastructure.repositories.sql_payment_method_repository import SQLPaymentMethodRepository
from config import settings
from application.dto.auth_dto import UserAuthDTO
from application.use_cases.transaction_use_cases import TransactionUseCases
from infrastructure.repositories.sql_transaction_repository import SQLTransactionRepository
from domain.models.transaction import Transaction

router = APIRouter()


@router.post("/request_payment_token", response_model=dict)
async def request_payment_token(
        payload: TwoCTwoPRequestPaymentRequest,
        user_auth: UserAuthDTO = Depends(get_current_user_auth),
        db: AsyncSession = Depends(get_db),
        payment_service: PaymentUseCases = Depends(get_payment_use_cases)

):

    payment_method_repository = SQLPaymentMethodRepository(db)
    payment_method_service = PaymentMethodUseCases(payment_method_repository=payment_method_repository)

    payment_methods = await payment_method_service.get_by_user_id(user_auth.user.id)
    customer_tokens = [item.payment_token for item in payment_methods]

    payment_dto = PaymentBase(
        type=PAYMENT_TYPE_CREDIT_CARD,
        amount=payload.amount,
        invoice_no=payload.invoiceNo,
        success=False,
        user_id=user_auth.user.id
    )
    new_payment = await payment_service.add(payment_dto, user_auth.user.id)
    if new_payment is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong Payment")
    
    payment_token_response = await payment_service.request_payment(amount=payload.amount, name=payload.name, desc=payload.description, invoiceNo=payload.invoiceNo, customerToken=customer_tokens)
    if payment_token_response is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong Request Payment")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": payment_token_response.__dict__
    }

@router.post("/complete_payment", response_model=dict)
async def complete_payment(
        body: TwoCTwoPPaymentWebHookRequest,
        db: AsyncSession = Depends(get_db),
        payment_service: PaymentUseCases = Depends(get_payment_use_cases)
):
    print("complete payment payload start")
    print(body.payload)
    print("complete payment payload end")

    payment_method_repository = SQLPaymentMethodRepository(db)
    payment_method_service = PaymentMethodUseCases(payment_method_repository=payment_method_repository)
    transaction_repository = SQLTransactionRepository(db)
    transaction_use_cases = TransactionUseCases(transaction_repository)

    payment_response = decode_payment_result_token(body.payload)
    payment = await payment_service.get_by_invoice_no(payment_response.invoiceNo)
    if payment is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong Payment")
    payment_dto = PaymentBase(
        user_id=payment.user_id,
        amount=payment_response.amount,
        invoice_no=payment_response.invoiceNo,
        success=payment_response.respCode == '0000',
        order_id=payment.order_id,
        transaction_id=payment.transaction_id,
        description=payment.description,
        type=payment.type,
        raw_data=payment_response.__dict__
    )
    paymentUpdateResult = await payment_service.update_payment(id=payment.id, payment_update_dto=payment_dto)
    if paymentUpdateResult is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Payment Update Unsuccessful")
    
    transaction_id_splitted = payment_response.invoiceNo.split("-")
    transaction_id = int(transaction_id_splitted[1]) if transaction_id_splitted.__len__() > 1 and transaction_id_splitted[0] == 'crm' else None
    if transaction_id:
        transaction_update_dto = Transaction(
            is_paid = True
        )
        is_transaction_updated = await transaction_use_cases.update_transaction(transaction_id, 1, transaction_update_dto)
        print("is transaction updated: ", is_transaction_updated)
    
    if payment_response.customerToken != None:
        existed = await payment_method_service.get_by_user_id(payment.user_id)
        if existed == None or existed.__len__() == 0:
            cardType = payment_response.cardType
            if payment_response.cardType == 'CREDIT' and payment_response.accountNo != None:
                cardType = 'Visa' if payment_response.accountNo[0] == '4' else 'Mastercard' if payment_response.accountNo[0] == '2' or payment_response.accountNo[0] == '5' else None
            payment_method_dto = PaymentMethodBase(
                user_id=payment.user_id,
                payment_token=payment_response.customerToken,
                card_type=cardType,
                card_last_four=payment_response.accountNo[-4:] if payment_response.accountNo != None else None,
                expiry_date=datetime.strptime(payment_response.customerTokenExpiry, "%Y%m%d") if payment_response.customerTokenExpiry != None else None
            )
            paymentMethodCreationResult = await payment_method_service.add(payment_method_dto)
            if paymentMethodCreationResult is False:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Payment Method Create Unsuccessful")

    return {
        "error_message": None,
        "success": payment,
        "error_code": None,
        "result": payment
    }

@router.post("/paynow/", response_model=dict)
def generate_paynow(
        paynow: Paynow,
        db: AsyncSession = Depends(get_db),
        payment_service: PaymentUseCases = Depends(get_payment_use_cases)
):

    paynow_qr = payment_service.generate_payment_string(paynow)
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": paynow_qr
    }

@router.post("/redirect_payment_success")
def redirect_payment_success(paymentResponse: str = Form(...)):
    redirect_url = f"{settings.PAYMENT_SUCCESS_URL}?paymentResponse={paymentResponse}"
    return RedirectResponse(url=redirect_url, status_code=302)

