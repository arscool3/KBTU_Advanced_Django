import dramatiq

@dramatiq.actor
def send_notifications(user_id, message):
    from ..db.session import SessionLocal
    from ..models import Notification
    db = SessionLocal()
    try:
        notification = Notification(user_id=user_id, message=message)
        db.add(notification)
        db.commit()
    finally:
        db.close()
