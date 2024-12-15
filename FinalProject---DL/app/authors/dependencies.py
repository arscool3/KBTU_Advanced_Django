from fastapi import Depends
from sqlalchemy.orm import Session

from app.authors.schemas import CreateAuthor
from app.database import get_db
from app.utils.dependencies import BaseDependency


class AuthorCreateDependency(BaseDependency):

    def __call__(self, body: CreateAuthor, session: Session = Depends(get_db)):
        self.repo.session = session
        return self.repo.create(body)