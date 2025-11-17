from abc import ABC, abstractmethod
from typing import Optional, List, Union
from domain.models.user import User, UpdatePassword, UserBase, DeleteUser
from infrastructure.orm.user_qr_keys_orm_model import UserQrKeysOrmModel
from domain.models.user_message import UserMessage


class UserRepository(ABC):
    @abstractmethod
    async def add_user(self, user: User) -> bool:
        pass

    @abstractmethod
    async def add_user_admin(self, tenant_id: int, user_admin: User) -> bool:
        pass

    @abstractmethod
    async def register(self, user: User) -> None:
        pass

    @abstractmethod
    async def get_by_full_mobile(self, full_mobile: str) -> Optional[User]:
        pass

    @abstractmethod
    async def get_by_id(self, user_id: int) -> Union[User, None]:
        pass

    @abstractmethod
    async def get_all(self, current_user: dict) -> List[User]:
        pass

    @abstractmethod
    async def update_password(self, update_password: UpdatePassword, current_user: dict) -> bool:
        pass

    @abstractmethod
    async def update_user_info(self,id:int, update_user: UserBase, current_user: dict) -> bool:
        pass

    @abstractmethod
    async def delete_user(self, user_id: int, current_user: dict) -> bool:
        pass

    @abstractmethod
    async def get_profile(self, current_user: dict) -> Union[User, None]:
        pass

    @abstractmethod
    async def get_qr_code(self, current_user: dict, key_name: str) -> str:
        pass

    @abstractmethod
    async def get_user_qr_key(self, key_name) -> UserQrKeysOrmModel:
        pass

    @abstractmethod
    async def get_active_key_name(self) -> str:
        pass

    @abstractmethod
    async def save_message(self, user_message: UserMessage) -> None:
        pass
    
    @abstractmethod
    async def get_user_messages(self, user_id: int) -> List[UserMessage]:
        pass
