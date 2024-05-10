import dramatiq
from dramatiq.brokers.redis import RedisBroker
from database.database import SessionLocal, User
from email_config import EmailSender
import logging

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

redis_broker = RedisBroker(host="localhost", port=6379)
dramatiq.set_broker(redis_broker)
sender = EmailSender()

@dramatiq.actor
def send_notification(recipient, **data):
    if data.get('user_id') is None:
        logging.error('TRY NEXT TIME')
        return
    if recipient is None:
        logging.error('USER DOES NOT EXISTS')
        return
    sender.send_message(recipient, data.get('title'), data.get('message'))
