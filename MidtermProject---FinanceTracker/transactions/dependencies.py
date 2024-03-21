from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from transactions.schemas import CreateTransaction
from utils.dependencies import BaseDependency


class TransactionCreateDependency(BaseDependency):

    def __call__(self, body: CreateTransaction, session: Session = Depends(get_db)):
        self.repo.session = session
        return self.repo.create(body)
