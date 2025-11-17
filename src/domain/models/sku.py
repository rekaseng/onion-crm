from pydantic import BaseModel
from typing import Optional, TypedDict
from datetime import datetime

class SkuBase(BaseModel):
    name: str
    sku: str
    source_id: int
    is_deleted: bool = False


class Sku(SkuBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    deleted_by: Optional[int] = None

class HQSku(TypedDict):
    id: int
    name: str
    active: bool
