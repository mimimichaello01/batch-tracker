from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional

from uuid import UUID

from app.domain.entities.batch import BatchEntity


class AbstractBatchRepository(ABC):
    @abstractmethod
    async def get_batch_by_oid(self, batch_oid: UUID) -> Optional[BatchEntity]: ...

    @abstractmethod
    async def get_batches_by_filter(
        self,
        *,
        is_closed: Optional[bool] = None,
        batch_number: Optional[int] = None,
        work_center: Optional[str] = None
    ) -> List[BatchEntity]: ...

    @abstractmethod
    async def get_by_number_and_date(
        self, batch_number: int, batch_date: date
    ) -> Optional[BatchEntity]: ...

    @abstractmethod
    async def get_all_batch(self) -> List[BatchEntity]: ...

    @abstractmethod
    async def add_batch(self, batch: BatchEntity) -> BatchEntity: ...

    @abstractmethod
    async def update_batch(
        self, batch_oid: UUID, batch: BatchEntity
    ) -> Optional[BatchEntity]: ...

    @abstractmethod
    async def delete_batch(self, batch_oid: UUID) -> None: ...

    @abstractmethod
    async def get_product_codes_by_batch(self, batch_oid: UUID) -> list[str]: ...
