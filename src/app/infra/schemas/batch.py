from pydantic import BaseModel
from uuid import UUID
from datetime import datetime, date
from typing import Optional


class BatchCreateSchema(BaseModel):
    is_closed: bool
    shift_task_name: str
    work_center: str
    shift: str
    brigade: str
    batch_number: int
    batch_date: date
    nomenclature: str
    ekn_code: str
    rc_identifier: str
    shift_start_datetime: datetime
    shift_end_datetime: datetime

    class Config:
        from_attributes = True

class UpdateBatchSchema(BaseModel):
    shift_task_name: Optional[str] = None
    work_center: Optional[str] = None
    shift: Optional[str] = None
    brigade: Optional[str] = None
    batch_number: Optional[int] = None
    batch_date: Optional[date] = None
    nomenclature: Optional[str] = None
    ekn_code: Optional[str] = None
    rc_identifier: Optional[str] = None
    shift_start_datetime: Optional[datetime] = None
    shift_end_datetime: Optional[datetime] = None
    is_closed: Optional[bool] = None


class BatchResponseSchema(BatchCreateSchema):
    oid: UUID
    closed_at: Optional[datetime] = None
    product_codes: list[str]

    class Config:
        from_attributes = True
