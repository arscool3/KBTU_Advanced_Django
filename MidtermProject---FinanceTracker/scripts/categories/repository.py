from sqlalchemy.orm import Session

from scripts.categories import schemas
from models import Category
from utils.repository import BaseRepository


class CategoryRepo(BaseRepository):
    model = Category
    session = Session
    schema = schemas.Category
