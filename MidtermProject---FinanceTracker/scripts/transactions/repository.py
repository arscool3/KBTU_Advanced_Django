from sqlalchemy.orm import Session

from models import Transaction
from scripts.transactions import schemas
from utils.repository import BaseRepository


class TransactionRepo(BaseRepository):
    model = Transaction
    session = Session
    schema = schemas.Transaction
