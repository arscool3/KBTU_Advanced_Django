from cart.schemas import Cart
from helpers import BaseSchema
from product.schemas import Product


class BaseCartItem(BaseSchema):
    amount: int


class CartItem(BaseCartItem):
    id: int
    product: Product
    cart: Cart


class CreateCartItem(BaseCartItem):
    cart_id: int
    product_id: int
    amount: int
