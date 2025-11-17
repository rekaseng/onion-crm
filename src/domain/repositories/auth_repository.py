from abc import ABC, abstractmethod
from domain.models.login import Login, Token, Message, NewPassword


class AuthRepository(ABC):
    @abstractmethod
    async def login_access_token(self, form_data: Login) -> Token:
        pass

    @abstractmethod
    async def reset_password(self, body: NewPassword) -> Message:
        pass
