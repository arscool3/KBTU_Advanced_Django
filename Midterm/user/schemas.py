from cart.schemas import Cart
from helpers import BaseSchema


class BaseProduct(BaseSchema):
    name: str
    email: str


class User(BaseProduct):
    id: int
    cart: Cart


class CreateUser(BaseProduct):
    pass