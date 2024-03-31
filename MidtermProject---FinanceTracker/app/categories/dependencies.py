from fastapi import Depends
from sqlalchemy.orm import Session

from app.categories.schemas import CreateCategory
from app.database import get_db
from app.utils.dependencies import BaseDependency


class CategoryCreateDependency(BaseDependency):

    def __call__(self, body: CreateCategory, session: Session = Depends(get_db)):
        self.repo.session = session
        return self.repo.create(body)
