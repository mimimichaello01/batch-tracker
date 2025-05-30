from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from uuid import UUID

from app.domain.entities.batch import BatchEntity
from app.infra.api.dependencies import (
    get_add_batch_product_use_case,
    get_aggregate_batch_product_use_case,
    get_batch_by_id_use_case,
    get_batches_by_filter_use_case,
    get_create_batch_use_case,
    get_update_batch_use_case,
)
from app.infra.db.mappers.batch_mapper import batch_create_schema_to_entity
from app.infra.db.mappers.product_mapper import product_add_schema_to_entity, product_orm_to_entity
from app.infra.schemas.batch import (
    BatchCreateSchema,
    BatchResponseSchema,
    UpdateBatchSchema,
)
from app.infra.schemas.product_item import AggregationInput, AggregationOutput, ProductItemAddSchema, ProductItemResponse
from app.use_cases.batch_use_cases import (
    AddBatchProductUseCase,
    AggregateBatchProductsUseCase,
    CreateBatchUseCase,
    GetBatchByIdUseCase,
    GetBatchesByFilterUseCase,
    UpdateBatchUseCase,
)
from app.use_cases.exceptions.exceptions import BatchNotFoundException


batch_router = APIRouter(prefix="/batches", tags=["Batches"])


@batch_router.post("/add", response_model=BatchResponseSchema)
async def create_batch(
    create_batch: BatchCreateSchema,
    use_case: CreateBatchUseCase = Depends(get_create_batch_use_case),
):
    batch_entity = batch_create_schema_to_entity(create_batch)
    created_batch = await use_case.execute(batch_entity)
    return created_batch


@batch_router.get("/{batch_oid}", response_model=BatchResponseSchema)
async def get_batch_by_id(
    batch_oid: UUID,
    use_case: GetBatchByIdUseCase = Depends(get_batch_by_id_use_case),
):
    try:
        return await use_case.execute(batch_oid)
    except BatchNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@batch_router.get("/", response_model=List[BatchEntity])
async def get_batches_by_filter(
    is_closed: Optional[bool] = Query(None),
    batch_number: Optional[int] = Query(None),
    work_center: Optional[str] = Query(None),
    use_case: GetBatchesByFilterUseCase = Depends(get_batches_by_filter_use_case),
):
    try:
        batch_entity = await use_case.execute(
            is_closed=is_closed, batch_number=batch_number, work_center=work_center
        )
        return batch_entity
    except BatchNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@batch_router.patch("/{batch_oid}", response_model=BatchResponseSchema)
async def update_batch(
    batch_oid: UUID,
    patch_data: UpdateBatchSchema,
    use_case: UpdateBatchUseCase = Depends(get_update_batch_use_case),
):
    try:
        updated_batch = await use_case.execute(batch_oid, patch_data)
        return updated_batch
    except BatchNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@batch_router.post("/product", response_model=List[ProductItemResponse])
async def add_product_item(
    create_products: List[ProductItemAddSchema],
    use_case: AddBatchProductUseCase = Depends(get_add_batch_product_use_case),
):
    result = []
    for product_data in create_products:
        product_entity = product_add_schema_to_entity(product_data)

        if await use_case.product_repo.get_by_unique_code(product_entity.unique_code):
            continue

        try:
            added_product = await use_case.execute(
                batch_number=product_data.batch_number,
                batch_date=product_data.batch_date,
                product=product_entity
            )
            result.append(added_product)
        except BatchNotFoundException:
            continue

    return result


@batch_router.post("/aggregate", response_model=AggregationOutput)
async def aggregate_product(
    data: AggregationInput,
    use_case: AggregateBatchProductsUseCase = Depends(get_aggregate_batch_product_use_case)
):
    unique_code = await use_case.execute(data.batch_oid, data.unique_code)
    return AggregationOutput(unique_code=unique_code)
