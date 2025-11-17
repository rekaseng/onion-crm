from abc import ABC, abstractmethod
from typing import Optional, List
from domain.models.refresh_token import RefreshToken, UpdateRefreshToken


class RefreshTokenRepository(ABC):
    @abstractmethod
    async def add(self, refresh_token: RefreshToken) -> bool:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[RefreshToken]:
        pass

    @abstractmethod
    async def get_all(self) -> List[RefreshToken]:
        pass

    @abstractmethod
    async def update_refresh_token(self, updateRefreshToken: UpdateRefreshToken) -> bool:
        pass

    @abstractmethod
    async def delete_refresh_token(self, id: int) -> bool:
        pass
