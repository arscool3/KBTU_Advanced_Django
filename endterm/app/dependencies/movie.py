from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import CreateMovie
from utils.dependencies import BaseDependency


class MovieCreateDependency(BaseDependency):

    def __call__(self, body: CreateMovie, session: Session = Depends(get_db)):
        self.repo.session = session
        return self.repo.create(body)
