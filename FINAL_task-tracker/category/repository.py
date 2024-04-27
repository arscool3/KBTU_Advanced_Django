from category import schemas
from category.models import Category
from utils.repository import BaseRepository


class CategoryRepo(BaseRepository):
    model = Category
    action_schema = {
        "list": schemas.Category,
        "retrieve": schemas.Category,
        "create": schemas.Category,
    }

