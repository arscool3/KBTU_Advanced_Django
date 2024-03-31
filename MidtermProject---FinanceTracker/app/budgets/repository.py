from sqlalchemy.orm import Session

from app.budgets import schemas
from app.models import Budget
from app.utils.repository import BaseRepository


class BudgetRepo(BaseRepository):
    model = Budget
    session = Session
    schema = schemas.Budget
