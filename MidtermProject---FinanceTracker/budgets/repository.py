from sqlalchemy.orm import Session

from budgets import schemas
from models import Budget
from utils.repository import BaseRepository


class BudgetRepo(BaseRepository):
    model = Budget
    session = Session
    schema = schemas.Budget
