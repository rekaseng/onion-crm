from abc import ABC, abstractmethod
from typing import Optional, List
from domain.models.sku import Sku, SkuBase
from infrastructure.orm.sku_orm_model import SkuOrmModel


class SkuRepository(ABC):
    @abstractmethod
    async def add(self, sku: Sku) -> bool:
        pass

    @abstractmethod
    def add_none_commit(self, sku: SkuOrmModel):
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[Sku]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Sku]:
        pass

    @abstractmethod
    async def get_all_orm(self) -> List[SkuOrmModel]:
        pass

    @abstractmethod
    async def commit(self) -> bool:
        pass

    @abstractmethod
    async def update_sku(self, id: int, update_sku: SkuBase, user_id: int) -> bool:
        pass

    @abstractmethod
    async def delete_sku(self, id: int, user_id: int) -> bool:
        pass
