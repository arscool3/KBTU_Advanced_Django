from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from task_comments.schemas import CreateTaskComment
from utils.dependencies import BaseDependency


class TaskCommentCreateDependency(BaseDependency):

    def __call__(self, body: CreateTaskComment, session: Session = Depends(get_db)):
        self.repo.session = session
        return self.repo.create(body)
