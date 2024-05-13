import dramatiq
from dramatiq.brokers.redis import RedisBroker
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



username = 'ваш_email@mail.ru'
password = 'ваш_пароль'
recipient = 'email_получателя@example.com'
smtp_server = 'smtp.mail.ru'
smtp_port = 465

redis_broker = RedisBroker(url="redis://localhost:6379")

dramatiq.set_broker(redis_broker)

@dramatiq.actor
def send_email(username: str, password: str, recipient: str, text: str):
    print(f"Sending email to {recipient}")
    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(username, password)
        msg = MIMEMultipart()
        msg['From'] = username
        msg['To'] = recipient
        msg['Subject'] = "Subject"
        body = text
        msg.attach(MIMEText(body, 'plain'))
        message = msg.as_string()
        server.sendmail(username, recipient, message)
        print("Email sended successfully")
    except Exception as e:
        print(f"Some error occured while sending email: {e}")
    finally:
        server.quit()
