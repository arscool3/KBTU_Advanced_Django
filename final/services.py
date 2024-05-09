from datetime import datetime, timedelta
from database import session
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status
from schemas import TokenData, EventCreate
from passlib.context import CryptContext
import models as db

SECRET_KEY = "2e398ac8a4e549cc5928d00f6ff3484f38c0e2c6c214cd7998d3e5922c84b56f6"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    try:
        yield session
        session.commit()
    except:
        raise
    finally:
        session.close()


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.ExpiredSignatureError:
        raise credentials_exception
    return token_data


def send_notification(event: EventCreate):
    camera = session.query(db.Camera).filter(db.Camera.id == event['camera_id']).first()
    event = session.query(db.Event).filter((db.Event.camera_id == event['camera_id']) & (db.Event.user_id == event['user_id'])).first()
    message = f"In camera that is located in {camera.location} breaking a rule! {event.description} "
    print(message)
    new_notification = db.Notification(message=message, event_id=event.id)
    session.add(new_notification)
    session.commit()