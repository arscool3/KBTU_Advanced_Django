from helpers import BaseSchema


class BaseProduct(BaseSchema):
    name: str
    description: str
    price: float
    amount: int


class Product(BaseProduct):
    id: int


class CreateProduct(BaseProduct):
    category_id: int
    firm_id: int
