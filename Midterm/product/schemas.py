from category.models import Category
from firm.models import Firm
from helpers import BaseSchema


class BaseProduct(BaseSchema):
    name: str
    description: str
    price: float
    category: Category


class Product(BaseProduct):
    id: int
    firm: Firm


class CreateProduct(BaseProduct):
    pass