from typing import List, Optional
from domain.repositories.transaction_repository import TransactionRepository
from domain.models.transaction import Transaction

class TransactionUseCases:
    def __init__(self, transaction_repository: TransactionRepository):
        self.transaction_repository = transaction_repository

    async def add_transaction(self, transaction: Transaction) -> bool:
        return await self.transaction_repository.add(transaction)

    async def get_transaction_by_id(self, id: int) -> Optional[Transaction]:
        return await self.transaction_repository.get_by_id(id)

    async def get_all(self) -> List[Transaction]:
        return await self.transaction_repository.get_all()

    async def update_transaction(self, id: int, user_id: int, transaction_update_dto: Transaction) -> bool:
        return await self.transaction_repository.update_transaction(id, user_id, transaction_update_dto)

    async def delete_transaction(self, id: int) -> bool:
        return await self.transaction_repository.delete_transaction(id)
