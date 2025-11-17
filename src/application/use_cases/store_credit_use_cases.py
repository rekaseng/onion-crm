from datetime import datetime
from typing import List

from application.dto.order_dto import OrderDeductAmountDto
from domain.models.store_credits import StoreCredit
from domain.models.store_credit_transaction import StoreCreditTransaction, StoreCreditTransactionType
from domain.repositories.store_credits_repository import StoreCreditsRepository


class StoreCreditUseCases:
    def __init__(self, store_credit_repository: StoreCreditsRepository):
        self.store_credit_repository = store_credit_repository

    async def get_all(self, current_user: dict) -> List[StoreCredit]:
        store_credits = await self.store_credit_repository.get_all(current_user)
        return store_credits
    
    async def get_by_user_id(self, user_id: int) -> List[StoreCredit]:
        store_credits = await self.store_credit_repository.get_by_user_id(user_id)
        return store_credits

    async def get_store_credits_balance(self, user_id: int) -> StoreCredit:
        store_credit = await self.store_credit_repository.get_store_credits_balance(user_id)
        return store_credit

    async def delete_store_credits_transaction(self, store_credits_transaction_id: int, current_user: dict) -> bool:
        store_credits = await self.store_credit_repository.delete_store_credits_transaction(
            store_credits_transaction_id, current_user)
        return store_credits

    async def manual_order_wallet_adjustment(self, admin_id: int, obj_in: OrderDeductAmountDto,  store_credit_type: StoreCreditTransactionType)-> bool:

        store_credit_transaction = StoreCreditTransaction(
            type=store_credit_type,
            description=obj_in.description,
            amount=obj_in.amount,
            store_credit_id=None, #repo will find by user_id and add it in
            order_id=obj_in.order_id,
            user_id=obj_in.customer_id,
            created_at=datetime.now(),
            updated_at=datetime.now(),

        )
        result = await self.store_credit_repository.add_transaction(
            admin_id,
            obj_in.customer_id,
            store_credit_transaction
        )

        return result