from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.transactions.schemas import CreateTransaction
from app.utils.dependencies import BaseDependency


class TransactionCreateDependency(BaseDependency):

    def __call__(self, body: CreateTransaction, session: Session = Depends(get_db)):
        self.repo.session = session
        return self.repo.create(body)
