from pydantic import BaseModel
from typing import List

from services.models import Product

class ProductListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    products: List[Product]
