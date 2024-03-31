from fastapi import Depends
from sqlalchemy.orm import Session

from app.accounts.schemas import CreateAccount
from app.database import get_db
from app.utils.dependencies import BaseDependency


class AccountCreateDependency(BaseDependency):

    def __call__(self, body: CreateAccount, session: Session = Depends(get_db)):
        self.repo.session = session
        return self.repo.create(body)
