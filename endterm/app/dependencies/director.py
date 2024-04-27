from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import CreateGenre, Director
from utils.dependencies import BaseDependency


class DirectorCreateDependency(BaseDependency):

    def __call__(self, body: Director, session: Session = Depends(get_db)):
        self.repo.session = session
        return self.repo.create(body)
