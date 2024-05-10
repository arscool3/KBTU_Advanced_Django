from db.session import SessionLocal
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.models.user import User
from config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db() -> Session:
    """
    Dependency для получения сессии базы данных.
    Создает новую сессию для каждого запроса и закрывает ее после завершения запроса.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_settings():
    """
    Dependency для получения глобальных настроек приложения.
    """
    return settings

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    """
    Dependency для аутентификации пользователя и получения информации о текущем пользователе.
    """
    user_id = decode_access_token(token)  # Функция декодирования токена не показана
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_kafka_producer():
    """
    Dependency для получения Kafka producer.
    """
    from .kafka.producer import KafkaProducerWrapper
    producer = KafkaProducerWrapper(servers=settings.KAFKA_SERVER)
    try:
        yield producer
    finally:
        producer.close()

# Здесь нужно добавить функцию oauth2_scheme и decode_access_token,
# если они используются для аутентификации и создания токенов.
# Это предполагает, что вы импортировали необходимые библиотеки для работы с JWT или другими токенами.
