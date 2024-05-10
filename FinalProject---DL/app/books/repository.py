from sqlalchemy.orm import Session

from app.books import schemas
from app.models import Book
from app.utils.repository import BaseRepository


class BookRepo(BaseRepository):
    model = Book
    session = Session
    schema = schemas.Book
