from datetime import date, datetime
import json
from http.client import HTTPException
from typing import List, Optional

from application.dto.auth_dto import UserAuthDTO
from application.dto.order_dto import OrderDeductAmountDto
from domain.models.transaction import Transaction
from domain.models.two_c_two_p_payments import TwoCTwoPDirectPaymentResponse, TwoCTwoPPaymentResponse, TwoCTwoPRequestPaymentPayload
from config import settings
from domain.repositories.payment_method_repository import PaymentMethodRepository
from domain.repositories.transaction_repository import TransactionRepository
from utils.constants import PAYMENT_TYPE_CREDIT_CARD, PAYMENT_TYPE_PAYNOW
from utils.security import create_payment_token, decode_payment_token
from http_client_helper import call_post_method_api
from domain.models.paynow import Paynow
from domain.repositories.payment_adapter import IPaymentAdapter
from domain.models.payment import Payment, PaymentBase
from domain.repositories.payment_repository import PaymentRepository


class PaymentUseCases:

    def __init__(self,
                 payment_repository: PaymentRepository,
                 payment_adapter: Optional[IPaymentAdapter] = None,
                 transaction_repository: Optional[TransactionRepository] = None,
                 payment_method_repository: Optional[PaymentMethodRepository] = None
    ):
        self.payment_repository = payment_repository
        self.payment_adapter = payment_adapter
        self.transaction_repository = transaction_repository
        self.payment_method_repository = payment_method_repository


    async def add(self, payment_dto: PaymentBase, user_id: int) -> bool:
        payment = Payment(
            created_at=datetime.now(),
            updated_at=datetime.now(),
            amount=payment_dto.amount,
            type=payment_dto.type,
            invoice_no=payment_dto.invoice_no,
            user_id=payment_dto.user_id,
            success=False,
            is_deleted=False,
            deleted_at=None,
            created_by=user_id,
            updated_by=user_id,
            deleted_by=None
        )
        payment = await self.payment_repository.add(payment)
        return payment
    
    async def get_by_invoice_no(self, invoice_no: str) -> Payment:
        payment = await self.payment_repository.get_by_invoice_no(invoice_no)
        return payment
    
    async def get_by_date_range(self, start_date: date, end_date: date) -> List[Payment]:
        payment = await self.payment_repository.get_by_date_range(start_date, end_date)
        return payment
    
    async def get_by_id(self, id: int) -> Optional[Payment]:
        return await self.payment_repository.get_by_id(id)
    
    async def get_by_user_id(self, user_id: int) -> List[Payment]:
        return await self.payment_repository.get_by_user_id(user_id)
    
    async def update_payment(self, id: int, payment_update_dto: PaymentBase) -> bool:
        payment = await self.payment_repository.update_payment(id, payment_update_dto)
        return payment

    async def request_payment(self, name: str, desc: str, invoiceNo: str, amount: float, customerToken: Optional[List[str]]) -> TwoCTwoPPaymentResponse:
        payload = TwoCTwoPRequestPaymentPayload(
            name = name,
            merchantID = settings.PAYMENT_MERCHANT_ID,
            invoiceNo = invoiceNo,
            description = desc,
            amount = amount,
            currencyCode = settings.PAYMENT_MERCHANT_CURRENCY_CODE,
            tokenize = customerToken.__len__() == 0,
            customerToken = customerToken,
            request3DS = 'N',
            paymentChannel=['CC']
        )
        tokenPayload = create_payment_token(payload=payload)
        response = await call_post_method_api(f'{settings.PAYMENT_URL}/paymentToken', {'payload': tokenPayload})
        if response.status_code == 200:
            return decode_payment_token(json.loads(response.text)['payload'])
        print("Request payment token failed.")
        return None
    
    async def request_card_payment(self, paymentToken: str, customerToken: Optional[List[str]]) -> TwoCTwoPDirectPaymentResponse:
        payload = {
            "payment": {
                "code": {
                    "channelCode": "CC"
                },
                "data": {
                    "customerToken": customerToken[customerToken.__len__() - 1]
                }
            },
            "paymentToken": paymentToken
        }
        response = await call_post_method_api(f'{settings.PAYMENT_URL}/payment', payload)
        if response.status_code == 200:
            resp_data = json.loads(response.text)
            return TwoCTwoPDirectPaymentResponse(
                data = resp_data['data'] if 'data' in resp_data else None,
                invoiceNo = resp_data['invoiceNo'] if 'invoiceNo' in resp_data else None,
                channelCode = resp_data['channelCode'],
                respCode = resp_data['respCode'],
                respDesc = resp_data['respDesc'],
            )
        print("Request payment token failed.")
        return None

    def generate_payment_string(self, paynow: Paynow)-> str:
        paynow_str =  self.payment_adapter.generate_payment_string(paynow)
        return paynow_str

    async def manual_order_card_payment(self, admin_id: int, obj_in: OrderDeductAmountDto )-> bool:
        new_transaction = Transaction(
            user_id=obj_in.customer_id,
            order_id=obj_in.order_id,
            amount=obj_in.amount,
            is_paid=False,
            payment_type=PAYMENT_TYPE_CREDIT_CARD,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            created_by=admin_id,
            updated_by=admin_id
        )
        created_transaction = await self.transaction_repository.add(new_transaction)

        payment = Payment(
            amount=obj_in.amount,
            invoice_no=created_transaction.transaction_ref,
            success=False,
            user_id=obj_in.customer_id,
            order_id=obj_in.order_id,
            transaction_id=created_transaction.id,
            type=PAYMENT_TYPE_CREDIT_CARD,
            description=obj_in.description,
            is_deleted=False,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            created_by=admin_id,
            updated_by=admin_id
        )
        new_payment = await self.payment_repository.add(payment)
        if not new_payment:
            raise HTTPException(status_code=400, detail="Payment Records not created")

        payment_methods = await self.payment_method_repository.get_by_user_id(obj_in.customer_id)
        customer_tokens = [item.payment_token for item in payment_methods]

        payment_token_response = await self.request_payment(
            amount=obj_in.amount,
            name=created_transaction.transaction_ref,
            desc=created_transaction.transaction_ref,
            invoiceNo=created_transaction.transaction_ref,
            customerToken=customer_tokens
        )

        if payment_token_response is None:
            raise HTTPException(status_code=400, detail="Wrong Request Payment")

        payment_token = payment_token_response.paymentToken
        payment_response = await self.request_card_payment(paymentToken=payment_token, customerToken=customer_tokens)

        if payment_response is None:
            raise HTTPException(status_code=400, detail="Wrong Direct Payment")

        return True


