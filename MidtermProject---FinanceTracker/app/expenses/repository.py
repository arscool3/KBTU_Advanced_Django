from sqlalchemy.orm import Session

from app.expenses import schemas
from app.models import Expense
from app.utils.repository import BaseRepository


class ExpenseRepo(BaseRepository):
    model = Expense
    session = Session
    schema = schemas.Expense
