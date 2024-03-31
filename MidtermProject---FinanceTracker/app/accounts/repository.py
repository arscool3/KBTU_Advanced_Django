from sqlalchemy.orm import Session

from app.accounts import schemas
from app.models import Account
from app.utils.repository import BaseRepository


class AccountRepo(BaseRepository):
    model = Account
    session = Session
    schema = schemas.Account
