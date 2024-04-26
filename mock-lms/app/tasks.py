import dramatiq
from .broker import kafka_broker
from .models.models import Enrollment
from .database.database import SessionLocal

dramatiq.set_broker(kafka_broker)


@dramatiq.actor
def process_enrollment(enrollment_id):
    db = SessionLocal()
    enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    if enrollment:
        print(f"Sending enrollment confirmation!")
    db.close()
