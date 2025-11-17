from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from api.deps import get_db, check_permission, get_current_user_auth
from application.use_cases.orders_use_cases import OrdersUseCases
from application.use_cases.sync_order_use_cases import SyncOrdersUseCases
from infrastructure.db.session import SessionLocalSync
from infrastructure.repositories.sql_orders_repository import SQLOrdersRepository
from domain.models.order import Order, OrderBase
from fastapi import HTTPException
from application.dto.auth_dto import UserAuthDTO
from infrastructure.repositories.sync.sql_sync_order_repository import SQLSyncOrderRepository
from infrastructure.repositories.sql_sku_repository import SQLSkuRepository
router = APIRouter()


@router.post("/", response_model=dict)
async def orders_add(
        orders_dto: OrderBase,
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        permission: bool = Depends(check_permission("orders_write")),
        db: AsyncSession = Depends(get_db)
):
    orders_repository = SQLOrdersRepository(db)
    sku_repository = SQLSkuRepository(db)
    orders_service = OrdersUseCases(orders_repository, sku_repository)
    new_orders = await orders_service.add(orders_dto, current_user.user.id, current_user.tenant.id)
    if new_orders is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong Order")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": []
    }

@router.post("/new", response_model=dict)
async def orders_add_new(
        message: dict,
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        permission: bool = Depends(check_permission("orders_write")),
        db: Session = Depends(get_db)
):
    db = SessionLocalSync()
    if 'subtotal' not in message:
        message['subtotal'] = 1
    if 'payment_amount' not in message:
        message['payment_amount'] = message['subtotal']  # Assuming full payment
    if 'payments' not in message:
        message['payments'] = []  # Empty list if payments are missing

    repository = SQLSyncOrderRepository(db)
    use_case = SyncOrdersUseCases(repository)
    for item in message['items']:
        item['sku_sku'] = item['sku_id']
    orders_dto = Order(**message)
    use_case.add_order(orders_dto)
    db.commit()
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result":True
    }

@router.get("/", response_model=dict)
async def get_all_orders(
        limit: int,
        offset: int,
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        permission: bool = Depends(check_permission("orders_read")),
        db: AsyncSession = Depends(get_db)
):
    orders_repository = SQLOrdersRepository(db)
    sku_repository = SQLSkuRepository(db)
    orders_service = OrdersUseCases(orders_repository, sku_repository)
    orders = await orders_service.get_all(limit, offset)
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": {"items": orders}
    }

@router.get("/get_my_orders", response_model=dict)
async def get_my_orders(
        current_user: UserAuthDTO = Depends(get_current_user_auth),
        db: AsyncSession = Depends(get_db)
):
    user_id  = current_user.user.id
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


@router.get("/{id}", response_model=dict)
async def get_by_id(
        id : int,
        db: AsyncSession = Depends(get_db)
):
    orders_repository = SQLOrdersRepository(db)
    sku_repository = SQLSkuRepository(db)
    orders_service = OrdersUseCases(orders_repository, sku_repository)
    order = await orders_service.get_by_id(id)
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": {"items": order}
    }
