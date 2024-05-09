import time
import models
import dramatiq

from dramatiq.results.backends.redis import RedisBackend
from dramatiq.brokers.redis import RedisBroker

result_backend = RedisBackend()
broker = RedisBroker()
dramatiq.set_broker(broker)


@dramatiq.actor()
def send_message_to_email(email: str, message: str):
    time.sleep(3)

    print(email, message)


def send_contribution_request_notification(contribution_id: int, user_id: int, db):
    user = db.query(models.User).filter_by(id=user_id).first()

    contribution = db.query(models.Contribution).filter_by(id=contribution_id).first()

    project = db.query(models.Project).filter_by(id=contribution.id).first()

    owner = db.query(models.User).filter_by(id=project.creator_id).first()

    message = f"Developer - {user.username} sent a contribution request for project {project.title}."

    send_message_to_email.send(owner.email, message)