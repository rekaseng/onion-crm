from typing import List

from domain.models.refresh_token import RefreshToken, RefreshTokenBase
from domain.repositories.refresh_token_repository import RefreshTokenRepository
from datetime import datetime


class RefreshTokenUseCases:
    def __init__(self, refresh_token_repository: RefreshTokenRepository):
        self.refresh_token_repository = refresh_token_repository

    async def add(self, refresh_token_dto: RefreshTokenBase, current_user: dict) -> bool:
        refresh_token = RefreshToken(
            created_at=datetime.now(),
            updated_at=datetime.now(),
            user_id=refresh_token_dto.user_id,
            refresh_token=refresh_token_dto.refresh_token,
            invalidate=refresh_token_dto.invalidate,
            expiry=refresh_token_dto.expiry,
            created_by=current_user["user"].id,
            updated_by=current_user["user"].id,
            deleted_by=None
        )
        await self.refresh_token_repository.add(refresh_token, current_user)
        return refresh_token

    async def get_all(self, current_user: dict) -> List[RefreshToken]:
        refresh_token = await self.refresh_token_repository.get_all(current_user)
        return refresh_token

    async def get_by_id(self, id: int, current_user: dict) -> RefreshToken:
        refresh_token = await self.refresh_token_repository.get_by_refresh_token(id, current_user)
        return refresh_token

    async def update_refresh_token(self, update_refresh_token_dto: RefreshTokenBase, current_user: dict) -> bool:
        refresh_token = await self.refresh_token_repository.update_refresh_token(update_refresh_token_dto, current_user)
        return refresh_token

    async def delete_refresh_token(self, id: int, current_user: dict) -> bool:
        refresh_token = await self.refresh_token_repository.delete_refresh_token(id, current_user)
        return refresh_token
