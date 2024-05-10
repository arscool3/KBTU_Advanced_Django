import time

import confluent_kafka

import models
import dramatiq

from database import session

from dramatiq.results.backends.redis import RedisBackend
from dramatiq.brokers.redis import RedisBroker

result_backend = RedisBackend()
broker = RedisBroker()
dramatiq.set_broker(broker)


consumer = confluent_kafka.Consumer(
    {"bootstrap.servers": "localhost:9092", "group.id": "main_group"}
)

topic = "contribution_requests_topic"
consumer.subscribe([topic])
number_of_messages = 10


def get_db():
    try:
        yield session
        session.commit()
    finally:
        session.close()


@dramatiq.actor()
def send_message_to_email(email: str, message: str):
    time.sleep(3)

    print(email, message)


def send_contribution_request_notification():
    try:
        while True:
            print('go')
            messages = consumer.consume(num_messages=number_of_messages, timeout=1.5)
            for message in messages:
                print(type(message), message)
    except Exception as e:
        print(f"Raised {e}")
    finally:
        consumer.close()

    # user = db.query(models.User).filter_by(id=user_id).first()
    #
    # contribution = db.query(models.Contribution).filter_by(id=contribution_id).first()
    #
    # project = db.query(models.Project).filter_by(id=contribution.id).first()
    #
    # owner = db.query(models.User).filter_by(id=project.creator_id).first()
    #
    # message = f"Developer - {user.username} sent a contribution request for project {project.title}."
    #
    # send_message_to_email.send(owner.email, message)


if __name__ == '__main__':
    send_contribution_request_notification()