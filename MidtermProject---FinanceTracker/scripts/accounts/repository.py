from sqlalchemy.orm import Session

from scripts.accounts import schemas
from models import Account
from utils.repository import BaseRepository


class AccountRepo(BaseRepository):
    model = Account
    session = Session
    schema = schemas.Account
