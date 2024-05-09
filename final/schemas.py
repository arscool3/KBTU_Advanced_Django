from datetime import datetime
from typing import List, Union

from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str

    class Config:
        from_attributes = True


class User(UserCreate):
    id: int


class TokenData(BaseModel):
    username: str = None


class NotificationBase(BaseModel):
    message: str


class Notification(NotificationBase):
    id: int
    event_id: int

    class Config:
        from_attributes = True


class EventCreate(BaseModel):
    description: str
    is_prohibited: bool
    user_id: int
    camera_id: int

    class Config:
        from_attributes = True


class Event(EventCreate):
    id: int
    timestamp: datetime
    notifications: List[Notification] = []

    class Config:
        from_attributes = True


class CameraCreate(BaseModel):
    location: str

    class Config:
        from_attributes = True


class Camera(CameraCreate):
    id: int


class LogCreate(BaseModel):
    data: str
    camera_id: int

    class Config:
        from_attributes = True


class Log(LogCreate):
    id: int
    camera: Camera


class NotificationCreate(BaseModel):
    message: str
    event_id: int

    class Config:
        from_attributes = True


class Notification(NotificationCreate):
    id: int


ReturnType = Union[User, Event]