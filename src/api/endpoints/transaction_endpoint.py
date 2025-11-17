from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from api.deps import get_db, get_current_user, check_permission, get_current_user_auth
from application.dto.auth_dto import UserAuthDTO
from application.use_cases.store_credit_use_cases import StoreCreditUseCases
from infrastructure.repositories.sql_store_credit_repository import SQLStoreCreditsRepository
from db_error_handlers import handle_db_errors
from domain.models.store_credit_transaction import StoreCreditTransactionBase, StoreCreditTransaction
from domain.models.store_credits import StoreCreditBase
from fastapi import HTTPException
from typing import List
from domain.models.transaction import Transaction
from application.use_cases.transaction_use_cases import TransactionUseCases
from infrastructure.repositories.sql_transaction_repository import SQLTransactionRepository
from infrastructure.repositories.sql_payment_repository import SQLPaymentRepository
import datetime

router = APIRouter()


@router.post("/start", response_model=dict)
async def transaction_start(
        db: AsyncSession = Depends(get_db),
        current_user: UserAuthDTO = Depends(get_current_user_auth),
):
    transaction_repository = SQLTransactionRepository(db)
    transaction_use_cases = TransactionUseCases(transaction_repository)
    new_transaction = Transaction(
        user_id=current_user.user.id,
        amount=0.0,
        is_paid=False,
        payment_type="",
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
        created_by=current_user.user.id,
        updated_by=current_user.user.id
    )

    created_transaction = await transaction_use_cases.add_transaction(new_transaction)
    if created_transaction is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Transaction creation failed")

    response = {
        'id': created_transaction.id,
        'transaction_ref': created_transaction.transaction_ref }
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": response
    }


@router.post("/get_transaction_payment/{transaction_id}", response_model=dict)
async def get_transaction_payment(
        transaction_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: UserAuthDTO = Depends(get_current_user_auth)
):
    # Initialize repositories
    payment_repository = SQLPaymentRepository(db)
    
    # Get payment by transaction_id
    payment = await payment_repository.get_by_transaction_id(transaction_id)
    
    # Check if payment exists and is successful
    payment_status = payment is not None and payment.success == True
    
    data = {
        "transaction_id": transaction_id,
        "payment_complete": payment_status
    }

    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": data
    }


@router.post("/add", response_model=dict)
async def add_transaction(
        transaction: Transaction,
        db: AsyncSession = Depends(get_db)
):
    transaction_repository = SQLTransactionRepository(db)
    transaction_use_cases = TransactionUseCases(transaction_repository)

    transaction.created_at = datetime.datetime.now()
    transaction.updated_at = datetime.datetime.now()
    transaction.created_by = transaction.user_id
    transaction.updated_by = transaction.user_id

    transaction = await transaction_use_cases.add_transaction(transaction)

    if transaction is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Transaction create failed")

    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": transaction
    }

@router.get("/{transaction_id}", response_model=dict)
async def get_transaction_by_id(
        transaction_id: int,
        db: AsyncSession = Depends(get_db)
):
    transaction_repository = SQLTransactionRepository(db)
    transaction_use_cases = TransactionUseCases(transaction_repository)

    transaction = await transaction_use_cases.get_transaction_by_id(transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": transaction
    }



@router.get("/", response_model=dict)
async def get_all_transactions(
        db: AsyncSession = Depends(get_db)
):
    transaction_repository = SQLTransactionRepository(db)
    transaction_use_cases = TransactionUseCases(transaction_repository)

    transactions = await transaction_use_cases.get_all()

    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": transactions  # Return the list directly here
    }



@router.put("/{transaction_id}", response_model=dict)
async def update_transaction(
        transaction_id: int,
        transaction_update: Transaction,
        user_auth: UserAuthDTO = Depends(get_current_user_auth),
        db: AsyncSession = Depends(get_db)
):
    transaction_repository = SQLTransactionRepository(db)
    transaction_use_cases = TransactionUseCases(transaction_repository)

    transaction = await transaction_use_cases.update_transaction(
        id=transaction_id,
        user_id=user_auth.user.id,
        transaction_update_dto=transaction_update
    )

    if transaction is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Transaction Update Unsuccessful")

    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": transaction_update
    }

@router.delete("/{transaction_id}", response_model=dict)
async def delete_transaction(
        transaction_id: int,
        db: AsyncSession = Depends(get_db)
):
    transaction_repository = SQLTransactionRepository(db)
    transaction_use_cases = TransactionUseCases(transaction_repository)

    transaction = await transaction_use_cases.delete_transaction(transaction_id)
    if transaction is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Transaction not found or cant be deleted")

    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": []
    }


