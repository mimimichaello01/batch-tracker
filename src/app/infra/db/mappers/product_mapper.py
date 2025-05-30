import uuid

from app.domain.entities.product_item import ProductItemEntity
from app.infra.db.models.models import ProductItemModel
from app.infra.schemas.product_item import ProductItemAddSchema

def product_orm_to_entity(product: ProductItemModel) -> ProductItemEntity:
    return ProductItemEntity(
        oid=str(product.oid),
        batch_oid=str(product.batch_oid),
        unique_code=product.unique_code,
        is_aggregated=product.is_aggregated,
        aggregated_at=product.aggregated_at
    )


def product_entity_to_orm(product: ProductItemEntity) -> ProductItemModel:
    return ProductItemModel(
        oid=uuid.UUID(product.oid),
        batch_oid=product.batch_oid,
        unique_code=product.unique_code,
        is_aggregated=product.is_aggregated,
        aggregated_at=product.aggregated_at
    )


def product_add_schema_to_entity(schema: ProductItemAddSchema) -> ProductItemEntity:
    return ProductItemEntity(
        unique_code=schema.unique_code,
        is_aggregated=False,
        aggregated_at=None
    )
