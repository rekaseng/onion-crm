from datetime import datetime
from typing import List, Optional
from domain.models.payment_method import PaymentMethod, PaymentMethodBase
from domain.repositories.payment_method_repository import PaymentMethodRepository


class PaymentMethodUseCases:
    def __init__(self, payment_method_repository: Optional[PaymentMethodRepository] = None):
        if payment_method_repository is not None:
            self.payment_method_repository = payment_method_repository

    async def add(self, payment_method_dto: PaymentMethodBase) -> bool:
        paymentMethod = PaymentMethod(
            created_at=datetime.now(),
            updated_at=datetime.now(),
            user_id=payment_method_dto.user_id,
            payment_token=payment_method_dto.payment_token,
            card_type=payment_method_dto.card_type,
            card_last_four=payment_method_dto.card_last_four,
            expiry_date=payment_method_dto.expiry_date,
            is_deleted=False,
            deleted_at=None,
            created_by=payment_method_dto.user_id,
            updated_by=payment_method_dto.user_id,
            deleted_by=None
        )
        paymentMethod = await self.payment_method_repository.add(paymentMethod)
        return paymentMethod
    
    async def get_by_user_id(self, user_id: int) -> Optional[List[PaymentMethod]]:
        return await self.payment_method_repository.get_by_user_id(user_id)
    
    async def get_by_payment_token(self, payment_token: str) -> Optional[PaymentMethod]:
        return await self.payment_method_repository.get_by_payment_token(payment_token)
    
    async def delete_payment_method(self, user_id: int) -> bool:
        return await self.payment_method_repository.delete_payment_method(user_id)