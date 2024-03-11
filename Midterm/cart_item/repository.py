from cart_item import schemas
from cart_item.models import CartItem
from repository import BaseRepository


class CartItemRepo(BaseRepository):
    model = CartItem
    action_schema = {
        "list": schemas.CartItem,
        "get_by_id": schemas.CartItem,
        "create": schemas.CreateCartItem
    }