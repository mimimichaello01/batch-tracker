from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from uuid import UUID

from application.interfaces.product_item_repository import AbstractProductItemRepository
from domain.entities.product_item import ProductItemEntity
from infra.db.converters.product_mapper import product_entity_to_orm, product_orm_to_entity
from infra.db.models.models import ProductItemModel






class ProductItemRepositoryImpl(AbstractProductItemRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_unique_code(self, unique_code: str) -> ProductItemEntity | None:
        result = await self.db.execute(
            select(ProductItemModel).where(ProductItemModel.unique_code == unique_code)
        )
        product_item_model = result.scalar_one_or_none()
        if not product_item_model:
            return None
        return product_orm_to_entity(product_item_model)

    async def add_product_item(self, product: ProductItemEntity) -> ProductItemEntity:
        product_item_model = product_entity_to_orm(product)
        self.db.add(product_item_model)
        await self.db.commit()
        await self.db.refresh(product_item_model)
        return product_orm_to_entity(product_item_model)

    async def update(self, product: ProductItemEntity):
        model = await self.db.get(ProductItemModel, product.oid)
        if not model:
            raise ValueError("Product not found")

        model.is_aggregated = product.is_aggregated
        model.aggregated_at = product.aggregated_at

        self.db.add(model)
        await self.db.commit()
