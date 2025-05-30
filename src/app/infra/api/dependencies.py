from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.infra.db.repositories.batch_repository_impl import BatchRepositoryImpl
from app.infra.db.repositories.interfaces.batch_repository import (
    AbstractBatchRepository,
)
from app.infra.db.repositories.interfaces.product_item_repository import AbstractProductItemRepository
from app.infra.db.repositories.product_item_repository_impl import ProductItemRepositoryImpl
from app.infra.db.session import get_db
from app.use_cases.batch_use_cases import AddBatchProductUseCase, AggregateBatchProductsUseCase, CreateBatchUseCase, GetBatchByIdUseCase, GetBatchesByFilterUseCase, UpdateBatchUseCase


def get_batch_repo(session: AsyncSession = Depends(get_db)) -> BatchRepositoryImpl:
    return BatchRepositoryImpl(session)

def get_product_item_repo(session: AsyncSession = Depends(get_db)) -> ProductItemRepositoryImpl:
    return ProductItemRepositoryImpl(session)


def get_create_batch_use_case(
    repo: AbstractBatchRepository = Depends(get_batch_repo),
) -> CreateBatchUseCase:
    return CreateBatchUseCase(repo)


def get_update_batch_use_case(
    repo: AbstractBatchRepository = Depends(get_batch_repo),
) -> UpdateBatchUseCase:
    return UpdateBatchUseCase(repo)


def get_batch_by_id_use_case(
    repo: AbstractBatchRepository = Depends(get_batch_repo),
) -> GetBatchByIdUseCase:
    return GetBatchByIdUseCase(repo)


def get_batches_by_filter_use_case(
    repo: AbstractBatchRepository = Depends(get_batch_repo)
) -> GetBatchesByFilterUseCase:
    return GetBatchesByFilterUseCase(repo)


def get_add_batch_product_use_case(
    batch_repo: AbstractBatchRepository = Depends(get_batch_repo),
    product_repo: AbstractProductItemRepository = Depends(get_product_item_repo)
) -> AddBatchProductUseCase:
    return AddBatchProductUseCase(batch_repo, product_repo)


def get_aggregate_batch_product_use_case(
    product_repo: AbstractProductItemRepository = Depends(get_product_item_repo)
) -> AggregateBatchProductsUseCase:
    return AggregateBatchProductsUseCase(product_repo)
