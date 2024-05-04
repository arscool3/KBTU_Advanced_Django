from celery import Celery
from sqlalchemy import select
from sqlalchemy.orm import Session

from config import REDIS_HOST, REDIS_PORT
from notifications.models import Notification
from notifications.schemas import CreateNotification
from tasks.models import Task
import smtplib
from email.message import EmailMessage
from config import SMTP_USER, SMTP_HOST, SMTP_PORT, SMTP_PASSWORD
from database import session
from journal.report_creator import CSVReportCreator
from users.models import User

celery = Celery(
    "tasks",
    broker=f"redis://{REDIS_HOST}:{REDIS_PORT}",
    backend=f"redis://{REDIS_HOST}:{REDIS_PORT}",
)


@celery.task
def create_task_notification_for_users(task_id: int):
    print("celery starting")
    db_session: Session = session()
    task = db_session.execute(select(Task).where(Task.id == task_id)).scalars().one()
    user_ids = db_session.execute(select(User.id).where(User.projects.contains(task.project))).scalars().all()

    notifications: list[Notification] = []
    for user_id in user_ids:
        notification = CreateNotification(message=_get_notification_message(task), user_id=user_id)
        notifications.append(
            Notification(**notification.model_dump()),
        )
    db_session.bulk_save_objects(notifications)
    db_session.commit()


def _get_notification_message(task: Task):
    return f"New task created: {task.title} - {task.description}"


@celery.task
def send_report_on_email(user_id: int):
    db_session = session()
    user = db_session.get(User, user_id)
    message = _get_email_msg(user.email)
    report_creator = CSVReportCreator(db_session, user)
    filename = report_creator.create_report()

    with open(f"./shared_storage/reports/{filename}", 'rb') as file:
        file_data = file.read()
        file_name = file.name
    message.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(message)


def _get_email_msg(user_email: str) -> EmailMessage:
    message = EmailMessage()
    message["Subject"] = "Task Tracker Report"
    message["From"] = SMTP_USER
    message["To"] = user_email
    message.set_content("""Here is your report on user actions in Task Tracker!!!""")
    return message


