from datetime import date, datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class ProductItemAddSchema(BaseModel):
    unique_code: str
    batch_number: int
    batch_date: date


class ProductItemResponse(BaseModel):
    oid: UUID
    batch_oid: UUID
    unique_code: str
    is_aggregated: bool
    aggregated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AggregationInput(BaseModel):
    batch_oid: UUID
    unique_code: str

class AggregationOutput(BaseModel):
    unique_code: str
