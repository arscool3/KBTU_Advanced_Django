import dramatiq
from dramatiq.brokers.redis import RedisBroker
from dramatiq.rate_limits.backends import RedisBackend
from dramatiq.results import Results
from sqlalchemy.orm import sessionmaker

from database import User, Notification, engine, Chat
from database import session

REDIS_URL = "redis://localhost:6379"

result_backend = RedisBackend()
broker = RedisBroker(url=REDIS_URL)
broker.add_middleware(Results(backend=result_backend))
dramatiq.set_broker(broker)

SyncSession = sessionmaker(engine)


@dramatiq.actor(max_retries=1)
def send_message_notification(chat_id: int, message_content: str):
    print(f"New Message from chat {chat_id}! : {message_content}.")


@dramatiq.actor(max_retries=1)
def save_notification_to_database(message_id: int, message_content: str):
    syn_session = SyncSession()
    try:
        notification = Notification(message_id=message_id, name=message_content)
        syn_session.add(notification)
        syn_session.commit()
        print("Notification saved")
    except Exception as e:
        syn_session.rollback()
        raise e
    finally:
        syn_session.close()


def notify_users_about_new_message(message_data: dict):
    sender_id = message_data.get('sender_id')
    content = message_data.get('content')
    message_id = message_data.get('id')
    chat_id = message_data.get('chat_id')
    users_to_notify = session.query(User.id).filter(User.id != sender_id, User.chats.has(Chat.id == chat_id)).all()
    # users_to_notify = session.query(User.id).filter(User.id != sender_id).all()

    for user_id, in users_to_notify:
        if user_id != sender_id:
            send_message_notification.send(user_id, content)
            save_notification_to_database.send(message_id, content)
            print("User notified")


# if __name__ == '__main__':
#     message_data = {'id': 439, 'sender_id': 3, 'content': 'new lesson'}
#     notify_users_about_new_message(message_data)


# Docker: 38b34a359f0d771d19ab0d5bf983643fa14e4c0ff5192dc641ed4f70b88a34d3
