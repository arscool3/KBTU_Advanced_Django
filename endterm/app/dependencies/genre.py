from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import CreateGenre
from utils.dependencies import BaseDependency


class GenreCreateDependency(BaseDependency):

    def __call__(self, body: CreateGenre, session: Session = Depends(get_db)):
        self.repo.session = session
        return self.repo.create(body)
