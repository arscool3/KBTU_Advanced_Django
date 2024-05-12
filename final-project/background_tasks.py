import dramatiq
from sqlalchemy import select
import logging
import models
import schemas
from database import session
from dramatiq.brokers.redis import RedisBroker

redis_broker = RedisBroker(url="redis://localhost:6379")
dramatiq.set_broker(redis_broker)

logger = logging.getLogger(__name__)


def get_event_by_id(event_id):
    db_event = session.query(models.Event).filter(models.Event.id == event_id).first()
    event = schemas.Event.model_validate(db_event)
    return event


def get_user_email(user_id):
    db_user = session.query(models.User).filter(models.User.id == user_id).first()
    user = schemas.User.model_validate(db_user)
    return user.email


@dramatiq.actor(queue_name="ticket_queue")
def process_purchase_task(user_id, event_id):
    db_event = session.query(models.Event).filter(models.Event.id == event_id).first()
    event = schemas.Event.model_validate(db_event)

    if not db_event:
        logger.error(f"Event {event_id} not found.")
        return

    if db_event.participants_current >= event.participants_max:
        logger.info(f"Event {event_id} is full.")
        return

    new_ticket = models.Ticket(user_id=user_id, event_id=event_id, status='Purchased')
    session.add(new_ticket)

    new_notification_schema = {'user_id': user_id, 'message': f'Event registration successful: {event.title}!'}
    new_notification = schemas.NotificationCreate(**new_notification_schema)
    session.add(models.Notification(**new_notification.model_dump()))

    session.commit()
    session.close()
    logger.info("Registered")
    send_email(user_id=user_id, event_id=event_id, title="Event registration successful!")


@dramatiq.actor(queue_name="cancellation_queue")
def notify_participants(user_id, event_id):
    event = get_event_by_id(event_id)
    new_notification_schema = {'user_id': user_id, 'message': f'Event cancelled!: {event.title}!'}
    new_notification = schemas.NotificationCreate(**new_notification_schema)
    session.add(models.Notification(**new_notification.model_dump()))
    session.commit()
    session.close()
    send_email(user_id=user_id, event_id=event_id, title='Event cancelled!')
    logger.info("Event cancelled!")


def send_email(user_id, event_id, title):
    email = get_user_email(user_id)
    event = get_event_by_id(event_id)
    print(f"{title},{event.title} to: {email}")