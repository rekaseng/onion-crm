from typing import Optional
from pydantic import BaseModel
from datetime import datetime, date


class MachineContractsBase(BaseModel):
    start_date: date
    end_date: date
    name: str
    is_deleted: bool = False


class MachineContracts(MachineContractsBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    machine_id: Optional[int] = None
    tenant_id: Optional[int] = None
    deleted_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    deleted_by: Optional[int] = None
