from helpers import BaseSchema
from product.schemas import Product


class BaseFirm(BaseSchema):
    name: str
    description: str


class Firm(BaseFirm):
    id: int
    products: list[Product]


class CreateFirm(BaseFirm):
    pass


