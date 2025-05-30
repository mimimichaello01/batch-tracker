from dataclasses import replace
from datetime import date, datetime, timezone
import uuid
from fastapi import HTTPException

from typing import List, Optional
from uuid import UUID
from app.domain.entities.batch import BatchEntity
from app.domain.entities.product_item import ProductItemEntity
from app.infra.db.repositories.interfaces.batch_repository import (
    AbstractBatchRepository,
)
from app.infra.db.repositories.interfaces.product_item_repository import AbstractProductItemRepository
from app.infra.schemas.batch import UpdateBatchSchema
from app.use_cases.exceptions.exceptions import BatchNotFoundException


class CreateBatchUseCase:
    def __init__(self, batch_repo: AbstractBatchRepository):
        self.batch_repo = batch_repo

    async def execute(self, batch: BatchEntity) -> BatchEntity:
        return await self.batch_repo.add_batch(batch)


class GetBatchByIdUseCase:
    def __init__(self, batch_repo: AbstractBatchRepository):
        self.batch_repo = batch_repo

    async def execute(self, batch_oid: UUID) -> BatchEntity:
        batch = await self.batch_repo.get_batch_by_oid(batch_oid)
        if not batch:
            raise BatchNotFoundException()

        product_codes = await self.batch_repo.get_product_codes_by_batch(
            batch_oid = uuid.UUID(batch.oid)
        )
        batch.product_codes = product_codes
        return batch


class UpdateBatchUseCase:
    def __init__(self, batch_repo: AbstractBatchRepository):
        self.batch_repo = batch_repo

    async def execute(self, batch_oid: UUID, patch_data: UpdateBatchSchema) -> BatchEntity:
        batch = await self.batch_repo.get_batch_by_oid(batch_oid)
        if not batch:
            raise BatchNotFoundException()

        self._apply_patch(batch, patch_data)


        updated_batch = await self.batch_repo.update_batch(batch_oid, batch)
        if not updated_batch:
            raise BatchNotFoundException()
        return updated_batch

    def _apply_patch(self, batch: BatchEntity, patch: UpdateBatchSchema) -> None:
        data = patch.model_dump(exclude_unset=True)

        for field, value in data.items():
            if field == "is_closed":
                batch.set_closed_status(value)
            else:
                setattr(batch, field, value)



class GetBatchesByFilterUseCase:
    def __init__(self, batch_repo: AbstractBatchRepository):
        self.batch_repo = batch_repo

    async def execute(
        self,
        is_closed: Optional[bool] = None,
        batch_number: Optional[int] = None,
        work_center: Optional[str] = None,
    ) -> List[BatchEntity]:
        batch = await self.batch_repo.get_batches_by_filter(
            is_closed=is_closed,
            batch_number=batch_number,
            work_center=work_center,
        )
        if not batch:
            raise BatchNotFoundException()
        return batch


class AddBatchProductUseCase:
    def __init__(self, batch_repo: AbstractBatchRepository, product_repo: AbstractProductItemRepository):
        self.batch_repo = batch_repo
        self.product_repo = product_repo

    async def execute(self, batch_number: int, batch_date: date, product: ProductItemEntity):
        batch = await self.batch_repo.get_by_number_and_date(batch_number, batch_date)
        if batch is None:
            raise BatchNotFoundException()

        batch.add_code(product)
        return await self.product_repo.add_product_item(product)

class AggregateBatchProductsUseCase:
    def __init__(self, product_repo: AbstractProductItemRepository):
        self.product_repo = product_repo

    async def execute(self, batch_oid: UUID, unique_code: str) -> str:
        product = await self.product_repo.get_by_unique_code(unique_code)
        if not product:
            raise HTTPException(status_code=404, detail="unique code not found")

        if str(product.batch_oid) != str(batch_oid):
            raise HTTPException(status_code=400, detail="unique code is attached to another batch")

        if product.is_aggregated:
            raise HTTPException(
                status_code=400,
                detail=f"unique code already used at {product.aggregated_at}"
            )

        product.is_aggregated = True
        product.aggregated_at = datetime.now(timezone.utc)

        await self.product_repo.update(product)
        return product.unique_code
