from sqlalchemy.orm import Session

from app.categories import schemas
from app.models import Category
from app.utils.repository import BaseRepository


class CategoryRepo(BaseRepository):
    model = Category
    session = Session
    schema = schemas.Category
