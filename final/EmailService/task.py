import smtplib
from email.message import EmailMessage
from celery import Celery
import config

celery = Celery('tasks', broker='redis://172.17.0.2:6379')


def get_email_template(username: str, rec_email: str, total: int, order_id: str, restaurant_id: str):
    email = EmailMessage()
    email['Subject'] = 'Test'
    email['From'] = config.SMTP_USER
    email['To'] = rec_email
    email.set_content(
        '<div>'
        f'<h1 style="color: red;">Hi, {username}, this is your check  😊</h1>'
        f'<p style="color: red;">order_id: {order_id}</p>'
        f'<p style="color: red;">restaurant_id: {restaurant_id}</p>'
        f'<p style="color: red;">Total sum: {total}</p>'
        '</div>',
        subtype='html'
    )
    return email


@celery.task
def send_email_check(username: str, email_req: str, total: int, order_id: str, restaurant_id: str):
    email = get_email_template(username, email_req, total, order_id, restaurant_id)
    with smtplib.SMTP_SSL(config.SMTP_HOST, config.SMTP_PORT) as server:
        server.login(config.SMTP_USER, config.SMTP_PASSWORD)
        server.send_message(email)


# celery -A task:celery worker --loglevel=INFO

# celery -A task:celery flower
