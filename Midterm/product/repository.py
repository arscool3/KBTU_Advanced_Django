from product import schemas
from product.models import Product
from repository import BaseRepository


class ProductRepo(BaseRepository):
    model = Product
    action_schema = {
        "list": schemas.Product,
        "get_by_id": schemas.Product,
        "create": schemas.CreateProduct
    }