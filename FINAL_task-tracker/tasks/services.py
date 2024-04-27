from sqlalchemy import select
from sqlalchemy.orm import Session

from notifications.models import Notification
from notifications.schemas import CreateNotification
from tasks.schemas import Task
from users.models import User


class TaskCreateNotifier:
    def __init__(self, session: Session):
        self.session = session

    def create_notification(self, task: Task):
        user_ids = self.session.execute(select(User.id).where(User.project_id == task.project.id)).scalars().all()

        notifications = []
        for user_id in user_ids:
            notification = CreateNotification(message=_get_notification_message(task), user_id=user_id)
            notifications.append(
                Notification(**notification.model_dump()),
            )

        self.session.bulk_save_objects(notifications)
        self.session.commit()


def _get_notification_message(task: Task):
    return f"New task created: {task.title} - {task.description}"
