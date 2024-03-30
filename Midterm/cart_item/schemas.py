from helpers import BaseSchema
from product.schemas import Product


class BaseCartItem(BaseSchema):
    amount: int


class CartItem(BaseCartItem):
    id: int
    product: Product


class CreateCartItem(BaseCartItem):
    cart_id: int
    product_id: int
    # amount: int
