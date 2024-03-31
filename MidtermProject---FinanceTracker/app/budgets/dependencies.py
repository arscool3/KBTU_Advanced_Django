from fastapi import Depends
from sqlalchemy.orm import Session

from app.budgets.schemas import CreateBudget
from app.database import get_db
from app.utils.dependencies import BaseDependency


class BudgetCreateDependency(BaseDependency):

    def __call__(self, body: CreateBudget, session: Session = Depends(get_db)):
        self.repo.session = session
        return self.repo.create(body)