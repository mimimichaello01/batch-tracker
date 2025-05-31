from dataclasses import dataclass, field
from datetime import datetime, date, timezone
from typing import Optional

from domain.entities.base import BaseEntity
from domain.entities.product_item import ProductItemEntity
from domain.exceptions.batch_exceptions import ClosedPartyException, ProductIsAggregatedException




@dataclass
class BatchEntity(BaseEntity):
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
    closed_at: Optional[datetime] = None
    product_codes: list[str] = field(default_factory=list)

    def get_is_closed(self):
        return self.is_closed

    def set_closed_status(self, is_closed: bool):
        self.is_closed = is_closed
        if is_closed:
            self.closed_at = datetime.now(timezone.utc)
        else:
            self.closed_at = None

    def add_code(self, product_item: ProductItemEntity):
        if self.is_closed:
            raise ClosedPartyException()
        if product_item.is_aggregated:
            raise ProductIsAggregatedException()

        product_item.batch_oid = self.oid
