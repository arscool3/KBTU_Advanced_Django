from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas.notification import NotificationOut, NotificationCreate
from app.services.notification_service import NotificationService
router = APIRouter()

@router.post("/", response_model=NotificationOut)
def create_notification(notification: NotificationCreate, db: Session = Depends(get_db)):
    notification_service = NotificationService(db)
    return notification_service.create_notification(notification)

@router.get("/{notification_id}", response_model=NotificationOut)
def read_notification(notification_id: int, db: Session = Depends(get_db)):
    notification_service = NotificationService(db)
    db_notification = notification_service.get_notification_by_id(notification_id)
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return db_notification
