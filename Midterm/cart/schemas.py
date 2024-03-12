from cart_item.schemas import CartItem
from helpers import BaseSchema


class Cart(BaseSchema):
    cart_items: list[CartItem]


class CreateCart(BaseSchema):
    user_id: int

