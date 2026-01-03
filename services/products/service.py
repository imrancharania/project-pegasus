from typing import List
from libs.core.factory import create_store
from libs.core.settings import PegasusSettings
from services.models import Product


class ProductsService:
    def __init__(self, settings: PegasusSettings) -> None:
        self.store = create_store(settings)

    def get_product_by_id(self, product_id: str) -> Product:
        pass

    def get_products(self) -> List[Product]:
        records = self.store.query(filters=None)

        products = [
            Product.model_validate(product)
            for idx, product in enumerate(list(records))
        ]

        return products

    def create_product(self, product: Product) -> None:
        pass

    def update_product(self, product_id: str, product: Product) -> None:
        pass

    def delete_product(self, product_id: str) -> None:
        pass
