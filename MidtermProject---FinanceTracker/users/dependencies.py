from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from users.schemas import CreateUser
from utils.dependencies import BaseDependency


class UserCreateDependency(BaseDependency):

    def __call__(self, body: CreateUser, session: Session = Depends(get_db)):
        self.repo.session = session
        return self.repo.create(body)
