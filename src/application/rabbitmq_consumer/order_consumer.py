import datetime
import asyncio
import math
from typing import List

from application.dto.order_consumer_dto import OrderConsumerDto, OrderConsumerItemDto, OrderConsumerCouponDto, OrderRewardPointDto
from application.dto.payment_dto import UserPaymentDto
from infrastructure.db.session import SessionLocalSync, SessionLocal
from fastapi import HTTPException

from infrastructure.external.paynow_adapter import PaynowAdapter
from infrastructure.repositories.sql_payment_method_repository import SQLPaymentMethodRepository
from infrastructure.repositories.sql_payment_repository import SQLPaymentRepository
from infrastructure.repositories.sql_transaction_repository import SQLTransactionRepository
from infrastructure.repositories.sync.sql_sync_order_repository import SQLSyncOrderRepository
from application.use_cases.sync_order_use_cases import SyncOrdersUseCases
from infrastructure.repositories.sync.sql_sync_payment_repository import SQLSyncPaymentRepository
from infrastructure.repositories.sync.sql_sync_payment_method_repository import SQLSyncPaymentMethodRepository
from domain.models.payment import Payment
from infrastructure.repositories.sync.sql_sync_transaction_repository import SQLSyncTransactionRepository
from domain.models.transaction import Transaction
from application.use_cases.payment_use_cases import PaymentUseCases
from infrastructure.repositories.sync.sql_sync_user_coupon_usage_repository import SQLSyncUserCouponUsageRepository
from domain.models.user_coupon_usage import UserCouponUsage
from infrastructure.repositories.sync.sql_sync_store_credit_repository import SQLSyncStoreCreditRepository
from infrastructure.repositories.sync.sql_sync_store_credit_transaction_repository import SQLSyncStoreCreditTransactionRepository
from domain.models.store_credits import StoreCredit
from domain.models.store_credit_transaction import StoreCreditTransaction, StoreCreditTransactionType
from infrastructure.repositories.sync.sql_sync_reward_point_repository import SQLSyncRewardPointRepository
from domain.models.reward_point import RewardPoint
from utils.constants import PAYMENT_TYPE_CREDIT_CARD, PAYMENT_TYPE_WALLET, PAYMENT_DESC_ORDER


def calculate_subtotal(items: List[OrderConsumerItemDto]):
    return sum(item.item_total for item in items)

def handle_wallet_payment(db, user_payment: UserPaymentDto, order_id: int):
    store_credit_repository = SQLSyncStoreCreditRepository(db)
    store_credit_transaction_repository = SQLSyncStoreCreditTransactionRepository(db)
    store_credit = StoreCredit(
        created_at = datetime.datetime.now(),
        updated_at = datetime.datetime.now(),
        user_id=user_payment.user_id,
        latest_amount=user_payment.subtotal,
        type=StoreCreditTransactionType.DEBIT,
        is_deleted=False
    )
    store_credit_id = store_credit_repository.upsert_sync(store_credit)
    store_credit_transaction = StoreCreditTransaction(
        type = StoreCreditTransactionType.DEBIT,
        amount = user_payment.subtotal,
        store_credit_id = store_credit_id,
        order_id = order_id,
        user_id = user_payment.user_id,
        description=PAYMENT_DESC_ORDER,
        created_at = datetime.datetime.now(),
        updated_at = datetime.datetime.now(),
    )
    store_credit_transaction_repository.add_sync(store_credit_transaction)
    return True

def handle_coupon_usage(db, coupon: OrderConsumerCouponDto, user_id: int):
    user_coupon_usage_repository = SQLSyncUserCouponUsageRepository(db)
    new_user_coupon_usage = UserCouponUsage(
        member_group_coupon_id = coupon.member_group_coupon_id,
        user_coupon_id = coupon.user_coupon_id,
        user_id = user_id,
        created_at = datetime.datetime.now()
    )
    user_coupon_usage_repository.add_sync(new_user_coupon_usage)

def handle_earn_reward_point(db, order_message: OrderConsumerDto, order_id: int):
    #todo:syd need to check reward rules.

    reward_point_repository = SQLSyncRewardPointRepository(db)
    latest_record = reward_point_repository.get_latest_by_user_id_sync(order_message.user_id)
    new_points = math.ceil(order_message.subtotal)
    new_reward_point = RewardPoint(
            created_at = datetime.datetime.now(),
            updated_at = datetime.datetime.now(),
            user_id=order_message.user_id,
            points=new_points,
            balance=(latest_record.balance if latest_record else 0) + new_points,
            order_id=order_id,
            type='credit',
            transaction_at=order_message.transaction_at,
            description=''
        )
    reward_point_repository.add_sync(new_reward_point)

def handle_reward_point(db, order_message: OrderConsumerDto, reward_point: OrderRewardPointDto, order_id: int):
    reward_point_repository = SQLSyncRewardPointRepository(db)
    latest_record = reward_point_repository.get_latest_by_user_id_sync(order_message.user_id)
    new_reward_point = RewardPoint(
        created_at = datetime.datetime.now(),
        updated_at = datetime.datetime.now(),
        user_id=order_message.user_id,
        points=reward_point.point,
        balance=(latest_record.balance if latest_record else 0) - reward_point.point,
        order_id=order_id,
        type='debit',
        transaction_at=order_message.transaction_at,
        description=''
    )
    reward_point_repository.add_sync(new_reward_point)

def request_direct_payment(db, user_payment: UserPaymentDto, order_id: int):
    async_db = SessionLocal()
    payment_repository = SQLPaymentRepository(async_db)
    paynow_adapter = PaynowAdapter()
    transaction_repository = SQLTransactionRepository(async_db)
    payment_method_repository = SQLPaymentMethodRepository(async_db)

    #todo:hoang, create another use_case for api request to 2c2p
    payment_service = PaymentUseCases(
        payment_repository=payment_repository,
        payment_adapter=paynow_adapter,
        transaction_repository=transaction_repository,
        payment_method_repository=payment_method_repository
    )

    payment_repository = SQLSyncPaymentRepository(db)
    payment_method_repository = SQLSyncPaymentMethodRepository(db)
    transaction_repository = SQLSyncTransactionRepository(db)
    payment_methods = payment_method_repository.get_by_user_id_sync(user_payment.user_id)
    customer_tokens = [item.payment_token for item in payment_methods]

    if customer_tokens.__len__() == 0:
        #todo:hoang save in db error_logs table
        #raise HTTPException(status_code=400, detail=f"Cannot pay because don't have customer token - user_id={user_payment.user_id}")
        return
    
    # create transaction
    new_transaction = Transaction(
        user_id=user_payment.user_id,
        order_id =order_id,
        amount=user_payment.subtotal,
        is_paid=False,
        payment_type=PAYMENT_TYPE_CREDIT_CARD,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
        created_by=1,
        updated_by=1
    )
    created_transaction = transaction_repository.add_sync(new_transaction)
    if created_transaction is None:
        raise HTTPException(status_code=400, detail="Transaction creation failed")

    payment_dto = Payment(
        amount=user_payment.subtotal,
        invoice_no=created_transaction.transaction_ref,
        transaction_id=created_transaction.id,
        type=PAYMENT_TYPE_CREDIT_CARD,
        description=PAYMENT_DESC_ORDER,
        success=False,
        user_id=user_payment.user_id,
        order_id=order_id,
        is_deleted=False,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now()
    )
    new_payment = payment_repository.add_sync(payment_dto)
    if new_payment is False:
        raise HTTPException(status_code=400, detail="Wrong Payment")
    
    payment_token_response = asyncio.run(payment_service.request_payment(amount=payment_dto.amount, name=payment_dto.invoice_no, desc=payment_dto.invoice_no, invoiceNo=payment_dto.invoice_no, customerToken=customer_tokens))
    if payment_token_response is None:
        raise HTTPException(status_code=400, detail="Wrong Request Payment")

    payment_token = payment_token_response.paymentToken
    payment_response = asyncio.run(payment_service.request_card_payment(paymentToken=payment_token, customerToken=customer_tokens))
    if payment_response is None:
        raise HTTPException(status_code=400, detail="Wrong Direct Payment")
    
    print("Direct payment request successfully:", payment_response.__dict__)


def order_consumer(message) -> None:
    # when use rewardPoints, it will be negative and there will be type "spend"
    db = SessionLocalSync()
    try:
        print("crm-order received:", message)

        order_message = OrderConsumerDto(**message)

        repository = SQLSyncOrderRepository(db)
        order_use_case = SyncOrdersUseCases(repository)

        # for item in message.items:
        #     item['sku_sku'] = item['sku_id']
        domain_order = order_message.to_domain_order()
        #todo:syd check order_ref duplicated
        new_order = order_use_case.add_order(domain_order)
        db.commit()
        # db.refresh(domain_order)


        for payment in domain_order.payments:

            user_payment_dto = UserPaymentDto(
                user_id=order_message.user_id,
                subtotal=payment.amount
            )

            # direct credit card payment
            if payment.type == PAYMENT_TYPE_CREDIT_CARD:
                request_direct_payment(db, user_payment_dto, new_order.id)

            #wallet
            if payment.type == PAYMENT_TYPE_WALLET:
                handle_wallet_payment(db, user_payment_dto, new_order.id)

        #coupons
        for coupon in order_message.coupons:
            handle_coupon_usage(db, coupon, order_message.user_id)

        for reward_point in order_message.reward_points:
            handle_reward_point(db, order_message, reward_point, domain_order.id)

        handle_earn_reward_point(db, order_message, domain_order.id)

    except HTTPException as e:
        print(f"HTTPException occurred: {e.detail} - Status code: {e.status_code}")

    except Exception as e:
        print(f"Error processing message: {e}")

    finally:
        db.close()


