
from celery import Celery

from app.database import SessionLocal
from app.models import Loan, Book, Reservation, Member

broker_url = 'redis://localhost:6379/0'

celery_app = Celery('tasks', broker=broker_url, backend=broker_url)

celery_app.conf.update(
    result_expires=3600,
)


# celery -A app.worker.celery_worker.celery_app worker --loglevel=info

@celery_app.task
def add(x, y):
    return x + y


@celery_app.task
def check_book_availability():
    db = SessionLocal()
    try:
        books = db.query(Book).all()
        for book in books:
            loaned_books = db.query(Loan).filter(Loan.book_id == book.id, Loan.status == 'active').count()
            reserved_books = db.query(Reservation).filter(Reservation.book_id == book.id,
                                                          Reservation.status == 'active').count()
            book.available_copies = reserved_books - loaned_books
        db.commit()
    finally:
        db.close()


@celery_app.task
def send_promotional_emails():
    db = SessionLocal()
    try:
        members = db.query(Member).all()
        for member in members:
            send_email(member.email, "Check Out Our New Arrivals!", "We have new books and services waiting for you!")
    finally:
        db.close()


def send_email(email, subject, message):
    print(f"Sending email to {email}: {subject} - {message}")
