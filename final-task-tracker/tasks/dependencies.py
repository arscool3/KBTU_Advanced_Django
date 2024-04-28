from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from journal.choices import RequestEnum
from journal.services import JournalWriter
from tasks.schemas import CreateTask
from tasks.services import TaskCreateNotifier

from utils.dependencies import BaseDependency


class TaskCreateDependency(BaseDependency):

    def __call__(self, body: CreateTask, session: Session = Depends(get_db)):
        self.repo.session = session
        task_created_logger = JournalWriter()
        task_create_notifier = TaskCreateNotifier(session)
        task = self.repo.create(body)

        task_created_logger.write_journal(
            data=task,
            method="POST",
            request=RequestEnum.ADD_TASK.value,
            user_id=task.user.id,
        )

        task_create_notifier.create_notification(task)
        return task
