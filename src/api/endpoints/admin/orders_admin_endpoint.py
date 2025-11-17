from datetime import date, timedelta, datetime
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.deps import get_db, get_current_user, check_permission, get_admin, get_current_user_auth
from api.di import get_payment_use_cases, get_store_credit_use_cases, get_communication_use_cases, get_user_use_cases
from application.dto.order_dto import OrderDeductAmountDto, OrderSendMessageDto
from application.use_cases.communication_use_cases import CommunicationUseCases
from application.use_cases.orders_use_cases import OrdersUseCases
from application.use_cases.payment_use_cases import PaymentUseCases
from application.use_cases.store_credit_use_cases import StoreCreditUseCases
from application.use_cases.user_use_cases import UserUseCases
from domain.models.store_credit_transaction import StoreCreditTransactionType
from infrastructure.repositories.sql_orders_repository import SQLOrdersRepository
from application.dto.auth_dto import UserAuthDTO
from utils.time_util import fomat_local_datetime
from infrastructure.repositories.sql_sku_repository import SQLSkuRepository

router = APIRouter()


@router.get("/history", response_model=dict)
async def get_all_admin_orders(
        limit: int,
        offset: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        permission: bool = Depends(check_permission("orders_read")),
        is_admin: bool = Depends(get_admin),
        db: AsyncSession = Depends(get_db)
):
    local_start = fomat_local_datetime(start_date)
    local_end =  fomat_local_datetime(end_date) + timedelta(days=1)

    orders_repository = SQLOrdersRepository(db)
    sku_repository = SQLSkuRepository(db)
    orders_service = OrdersUseCases(orders_repository, sku_repository)
    orders = await orders_service.get_all_admin(limit, offset, local_start, local_end)

    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": {"items":orders}
    }


@router.get("/get_by_user_id", response_model=dict)
async def get_by_user_id(
        user_id: int,
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        permission: bool = Depends(check_permission("orders_read")),
        is_admin: bool = Depends(get_admin),
        db: AsyncSession = Depends(get_db)
):

    orders_repository = SQLOrdersRepository(db)
    sku_repository = SQLSkuRepository(db)
    orders_service = OrdersUseCases(orders_repository, sku_repository)
    orders = await orders_service.get_by_user_id(user_id)

    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": {"items":orders}
    }


@router.post("/deduct_wallet", response_model=dict)
async def deduct_wallet(
        obj_in: OrderDeductAmountDto,
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        permission: bool = Depends(check_permission("orders_read")),
        is_admin: bool = Depends(get_admin),
        db: AsyncSession = Depends(get_db),
        store_credit_service: StoreCreditUseCases = Depends(get_store_credit_use_cases)
):
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


@router.post("/deduct_credit_card", response_model=dict)
async def deduct_credit_card(
        obj_in: OrderDeductAmountDto,
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        permission: bool = Depends(check_permission("orders_read")),
        is_admin: bool = Depends(get_admin),
        db: AsyncSession = Depends(get_db),
        payment_service: PaymentUseCases = Depends(get_payment_use_cases)

):
    result = await payment_service.manual_order_card_payment(current_user.user.id, obj_in)

    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": result
    }


@router.get("/{id}", response_model=dict)
async def get_all_admin_orders(
        id: int,
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        permission: bool = Depends(check_permission("orders_read")),
        is_admin: bool = Depends(get_admin),
        db: AsyncSession = Depends(get_db)
):
    orders_repository = SQLOrdersRepository(db)
    orders_service = OrdersUseCases(orders_repository)
    order = await orders_service.get_by_id(id)
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": order
    }
