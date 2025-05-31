from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from domain.entities.base import BaseEntity




@dataclass
class ProductItemEntity(BaseEntity):
    unique_code: str
    is_aggregated: bool
    batch_oid: Optional[str] = None
    aggregated_at: Optional[datetime] = None

    def get_is_aggregated(self):
        return self.is_aggregated
