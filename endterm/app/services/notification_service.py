from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.notification import Notification
from app.schemas.notification import NotificationCreate

class NotificationService:
    def __init__(self, db: Session):
        self.db = db

    def create_notification(self, notification_data: NotificationCreate):
        """
        Создает новое уведомление в базе данных.
        """
        new_notification = Notification(
            user_id=notification_data.user_id,
            message=notification_data.message
        )
        self.db.add(new_notification)
        self.db.commit()
        self.db.refresh(new_notification)
        return new_notification

    def send_notification(self, notification_id: int):
        """
        Отправляет уведомление, указанное его ID.
        В реальном приложении этот метод мог бы интегрироваться с внешними сервисами,
        такими как почтовые серверы, SMS-шлюзы или push-уведомления.
        """
        notification = self.db.query(Notification).filter(Notification.id == notification_id).first()
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")

        send_email(to=notification.user.email, subject="New Notification", body=notification.message)

        notification.is_sent = True
        self.db.commit()

def send_email(to: str, subject: str, body: str):
    """
    Заглушка для функции отправки email.
    В реальной жизни здесь могла бы быть интеграция с SMTP сервером или сервисом типа SendGrid.
    """
    print(f"Sending email to {to}: {subject} - {body}")