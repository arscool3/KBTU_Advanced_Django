from datetime import datetime

from helpers import BaseSchema
from product.schemas import Product


class BaseAnalysProduct(BaseSchema):
    count: int


class AnalysProduct(BaseAnalysProduct):
    id: int
    product: Product
    calculated_at: datetime


class CreateAnalysProduct(BaseAnalysProduct):
    product_id: int
    product_name: str