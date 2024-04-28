from sqlalchemy.orm import Session

from celery_worker import create_task_notification_for_users
from journal.choices import RequestEnum
from journal.producer import produce_journal_message
from tasks.schemas import Task


class TaskCreateNotifier:
    def __init__(self, session: Session):
        self.session = session

    def create_notification(self, task: Task):
        create_task_notification_for_users.delay(task.id)
        print("celery executed")


class TaskJournalWriter:

    def write_journal(self, task: Task, method: str, request: str):
        produce_journal_message({
            "data": task.model_dump(),
            "method": method,
            "request": str(request),
            "user_id": task.user.id,
        })
