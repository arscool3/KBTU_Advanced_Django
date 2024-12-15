from sqlalchemy.orm import Session

from models import User
from scripts.users import schemas
from utils.repository import BaseRepository


class UserRepo(BaseRepository):
    model = User
    session = Session
    schema = schemas.User
