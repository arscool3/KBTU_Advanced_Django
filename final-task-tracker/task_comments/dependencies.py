from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from journal.choices import RequestEnum
from journal.services import JournalWriter
from task_comments.schemas import CreateTaskComment
from utils.dependencies import BaseDependency


class TaskCommentCreateDependency(BaseDependency):

    def __call__(self, body: CreateTaskComment, session: Session = Depends(get_db)):
        self.repo.session = session
        task_comment_created_logger = JournalWriter()
        comment = self.repo.create(body)

        task_comment_created_logger.write_journal(
            data=comment,
            method="POST",
            request=RequestEnum.ADD_TASK_COMMENT.value,
            user_id=comment.user.id,
        )
        return comment
