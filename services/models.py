from langchain_core.documents import Document
from pydantic import BaseModel


class Product(BaseModel):
    title: str
    description: str


class ProductDocument(Document):
    def __init__(self, product: Product) -> None:
        super().__init__(page_content=product.description, metadata=product.model_dump())
