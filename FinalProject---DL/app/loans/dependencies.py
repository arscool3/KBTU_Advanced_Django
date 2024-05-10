from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.loans.schemas import CreateLoan
from app.utils.dependencies import BaseDependency


class LoanCreateDependency(BaseDependency):

    def __call__(self, body: CreateLoan, session: Session = Depends(get_db)):
        self.repo.session = session
        return self.repo.create(body)
