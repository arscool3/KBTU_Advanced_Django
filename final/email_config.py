from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from dotenv import dotenv_values
import logging
config = dotenv_values('secrets.env')

class EmailSender:
    def __init__(self) -> None:
        self.username = config.get('EMAIL_LOGIN')
        self.password = config.get('EMAIL_PASSWORD')
        self.smtp_server = config.get('SMTP_SERVER')
        self.smtp_port = config.get('SMTP_PORT')
    
    def create_message(self, recipient: str, title: str, message: str):
        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = recipient
        msg['Subject'] = title
        body = message
        msg.attach(MIMEText(body, 'plain'))
        return msg

    def send_message(self, recipient: str, title: str, message: str):
        msg = self.create_message(recipient=recipient, title=title, message=message)
        try:
            server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
            server.login(self.username, self.password)
            text = msg.as_string()
            server.sendmail(self.username, recipient, text)
            logging.info("Письмо успешно отправлено!")
        except Exception as e:
            logging.error(f"Ошибка при отправке письма: {e}")
        finally:
            server.quit()