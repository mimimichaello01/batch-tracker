from datetime import date
from typing import List, Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.batch import BatchEntity
from app.infra.db.mappers.batch_mapper import batch_entity_to_orm, batch_orm_to_entity
from app.infra.db.models.models import BatchModel, ProductItemModel
from app.infra.db.repositories.interfaces.batch_repository import (
    AbstractBatchRepository,
)


class BatchRepositoryImpl(AbstractBatchRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_batch_by_oid(self, batch_oid: UUID) -> Optional[BatchEntity]:
        batch = await self.db.get(BatchModel, batch_oid)
        if not batch:
            return None
        return batch_orm_to_entity(batch)

    async def get_batches_by_filter(
        self,
        *,
        is_closed: Optional[bool] = None,
        batch_number: Optional[int] = None,
        work_center: Optional[str] = None
    ) -> List[BatchEntity]:
        query = select(BatchModel)
        if is_closed is not None:
            query = query.where(BatchModel.is_closed == is_closed)
        if batch_number is not None:
            query = query.where(BatchModel.batch_number == batch_number)
        if work_center is not None:
            query = query.where(BatchModel.work_center == work_center)


        batches = await self.db.execute(query)
        return [batch_orm_to_entity(batch) for batch in batches.scalars().all()]


    async def get_by_number_and_date(self, batch_number: int, batch_date: date) -> Optional[BatchEntity]:
        result = await self.db.execute(
            select(BatchModel).where(
                BatchModel.batch_number == batch_number,
                BatchModel.batch_date == batch_date
            )
        )
        batch_model = result.scalar_one_or_none()
        if not batch_model:
            return None
        return batch_orm_to_entity(batch_model)


    async def get_all_batch(self) -> List[BatchEntity]:
        batchs = await self.db.execute(select(BatchModel))
        return [batch_orm_to_entity(batch) for batch in batchs.scalars().all()]

    async def add_batch(self, batch: BatchEntity) -> BatchEntity:
        batch_model = batch_entity_to_orm(batch)
        self.db.add(batch_model)
        await self.db.commit()
        await self.db.refresh(batch_model)
        return batch_orm_to_entity(batch_model)

    async def update_batch(self, batch_oid: UUID, batch: BatchEntity) -> BatchEntity | None:
        batch_model = await self.db.get(BatchModel, batch_oid)
        if not batch_model:
            return None

        batch_model.is_closed = batch.is_closed
        batch_model.closed_at = batch.closed_at
        batch_model.shift_task_name = batch.shift_task_name
        batch_model.work_center = batch.work_center
        batch_model.shift = batch.shift
        batch_model.brigade = batch.brigade
        batch_model.batch_number = batch.batch_number
        batch_model.batch_date = batch.batch_date
        batch_model.nomenclature = batch.nomenclature
        batch_model.ekn_code = batch.ekn_code
        batch_model.rc_identifier = batch.rc_identifier
        batch_model.shift_start_datetime = batch.shift_start_datetime
        batch_model.shift_end_datetime = batch.shift_end_datetime

        await self.db.commit()
        await self.db.refresh(batch_model)
        return batch_orm_to_entity(batch_model)

    async def delete_batch(self, batch_oid: UUID) -> None:
        batch = await self.db.get(BatchModel, batch_oid)
        if batch:
            await self.db.delete(batch)
            await self.db.commit()

    async def get_product_codes_by_batch(self, batch_oid: UUID) -> list[str]:
        result = await self.db.execute(
            select(ProductItemModel.unique_code).where(
                ProductItemModel.batch_oid == batch_oid
            )
        )
        return [row[0] for row in result.all()]
