from fastapi import Depends
from sqlalchemy.orm import Session

from category.schemas import CreateCategory
from database import get_db
from journal.choices import RequestEnum
from journal.services import JournalWriter
from utils.dependencies import BaseDependency


class CategoryCreateDependency(BaseDependency):

    def __call__(self, body: CreateCategory, session: Session = Depends(get_db)):
        self.repo.session = session
        return self.repo.create(body)
