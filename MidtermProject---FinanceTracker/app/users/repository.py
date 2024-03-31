from sqlalchemy.orm import Session

from app.models import User
from app.users import schemas
from app.utils.repository import BaseRepository


class UserRepo(BaseRepository):
    model = User
    session = Session
    schema = schemas.User
