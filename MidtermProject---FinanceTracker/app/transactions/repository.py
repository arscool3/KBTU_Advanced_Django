from sqlalchemy.orm import Session

from app.models import Transaction
from app.transactions import schemas
from app.utils.repository import BaseRepository


class TransactionRepo(BaseRepository):
    model = Transaction
    session = Session
    schema = schemas.Transaction
