from sqlalchemy.orm import Session

from app.authors import schemas
from app.models import Author
from app.utils.repository import BaseRepository


class AuthorRepo(BaseRepository):
    model = Author
    session = Session
    schema = schemas.Author
