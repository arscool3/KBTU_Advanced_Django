from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from tasks.schemas import CreateTask
from utils.dependencies import BaseDependency


class TaskCreateDependency(BaseDependency):

    def __call__(self, body: CreateTask, session: Session = Depends(get_db)):
        self.repo.session = session
        return self.repo.create(body)
