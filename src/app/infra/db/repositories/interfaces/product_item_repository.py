from abc import ABC, abstractmethod

from app.domain.entities.product_item import ProductItemEntity


class AbstractProductItemRepository(ABC):
    @abstractmethod
    async def get_by_unique_code(self, unique_code: str) -> ProductItemEntity | None:
        ...

    @abstractmethod
    async def add_product_item(self, product: ProductItemEntity) -> ProductItemEntity:
        ...

    @abstractmethod
    async def update(self, product: ProductItemEntity):
        ...
