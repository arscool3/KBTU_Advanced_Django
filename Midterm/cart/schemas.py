from cart_item.schemas import CartItem
from helpers import BaseSchema
from user.schemas import User


class Cart(BaseSchema):
    user: User
    cart_items: list[CartItem]


class CreateCart(BaseSchema):
    user_id: int

