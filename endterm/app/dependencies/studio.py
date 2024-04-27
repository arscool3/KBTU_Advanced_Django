from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import CreateGenre, Studio
from utils.dependencies import BaseDependency


class StudioCreateDependency(BaseDependency):

    def __call__(self, body: Studio, session: Session = Depends(get_db)):
        self.repo.session = session
        return self.repo.create(body)
