from cart.models import Cart
from cart import schemas
from repository import BaseRepository


class CartRepo(BaseRepository):
    model = Cart
    action_schema = {
        "list": schemas.Cart,
        "get_by_id": schemas.Cart,
        "create": schemas.CreateCart
    }