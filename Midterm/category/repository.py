from category import schemas
from category.models import Category
from repository import BaseRepository


class CategoryRepo(BaseRepository):
    model = Category
    action_schema = {
        "list": schemas.Category,
        "get_by_id": schemas.Category,
        "create": schemas.CreateCategory
    }