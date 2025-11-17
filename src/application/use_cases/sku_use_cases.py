from typing import List, Optional

from domain.models.sku import Sku, SkuBase
from domain.repositories.sku_repository import SkuRepository
from datetime import datetime

from domain.repositories.hq_adapter import IHqAdapter
from infrastructure.orm.sku_orm_model import SkuOrmModel


class SkuUseCases:
    def __init__(self, sku_repository: SkuRepository, hq_adapter: Optional[IHqAdapter] = None):
        self.sku_repository = sku_repository
        self.hq_adapter = hq_adapter

    async def add(self, sku_dto: SkuBase, user_id: int) -> bool:
        sku = Sku(
            created_at=datetime.now(),
            updated_at=datetime.now(),
            name=sku_dto.name,
            sku=sku_dto.sku,
            is_deleted=False,
            deleted_at=None,
            created_by=user_id,
            updated_by=user_id,
            deleted_by=None
        )
        await self.sku_repository.add(sku)
        return sku

    async def get_all(self) -> List[Sku]:
        skus = await self.sku_repository.get_all()
        return skus

    async def get_by_id(self, id: int) -> Sku:
        sku = await self.sku_repository.get_by_id(id)
        return sku

    async def update_sku(self, id:int, update_sku_dto: SkuBase, user_id: int) -> bool:
        sku = await self.sku_repository.update_sku(id, update_sku_dto, user_id)
        return sku

    async def delete_sku(self, id: int, user_id: int) -> bool:
        sku = await self.sku_repository.delete_sku(id, user_id)
        return sku
    
    async def update_skus_from_hq(self) -> bool:
        hq_skus = await self.hq_adapter.get_all_skus()
        crm_skus = await self.sku_repository.get_all_orm()
        crm_sku_dict = {}
        for crm_sku in crm_skus:
            crm_sku_dict[crm_sku.sku] = crm_sku
        
        for hq_sku in hq_skus:
            sku = hq_sku['name'].split('-')[0].strip()
            name = hq_sku['name'].split('-')[1].strip()
            id  = hq_sku.get("id")
            if sku in crm_sku_dict:
                to_update_sku = crm_sku_dict[sku]
                to_update_sku.name = name
                to_update_sku.source_id = id
                to_update_sku.is_deleted = hq_sku['active'] == False
                to_update_sku.updated_at = datetime.now()
            else:
                new_sku = SkuOrmModel(
                    name = name,
                    sku = sku,
                    source_id = id,
                )
                self.sku_repository.add_none_commit(new_sku)
        return await self.sku_repository.commit()
