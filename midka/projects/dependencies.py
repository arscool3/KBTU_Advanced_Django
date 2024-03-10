from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from projects.schemas import CreateProject
from utils.dependencies import BaseDependency


class ProjectCreateDependency(BaseDependency):

    def __call__(self, body: CreateProject, session: Session = Depends(get_db)):
        self.repo.session = session
        return self.repo.create(body)
