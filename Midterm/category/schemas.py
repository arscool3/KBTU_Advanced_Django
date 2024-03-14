from helpers import BaseSchema
from product.schemas import Product


class BaseCategory(BaseSchema):
    name: str
    description: str


class Category(BaseCategory):
    id: int
    products: list[Product]


class CreateCategory(BaseCategory):
    pass
