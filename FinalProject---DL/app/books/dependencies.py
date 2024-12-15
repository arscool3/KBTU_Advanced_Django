from fastapi import Depends
from sqlalchemy.orm import Session

from app.books.schemas import CreateBook
from app.database import get_db
from app.utils.dependencies import BaseDependency


class BookCreateDependency(BaseDependency):

    def __call__(self, body: CreateBook, session: Session = Depends(get_db)):
        self.repo.session = session
        return self.repo.create(body)
