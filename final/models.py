from typing import Annotated
import sqlalchemy
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import func, ForeignKey
from datetime import datetime

from database import Base

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]


class User(Base):
    __tablename__ = 'users'
    id: Mapped[_id]
    username: Mapped[str] = mapped_column(sqlalchemy.String)
    password: Mapped[str] = mapped_column(sqlalchemy.String)
    events: Mapped[list['Event']] = relationship("Event", back_populates="user")


class Event(Base):
    __tablename__ = 'events'
    id: Mapped[_id]
    timestamp: Mapped[datetime] = mapped_column(default=func.now())
    description: Mapped[str] = mapped_column(sqlalchemy.String)
    is_prohibited: Mapped[bool] = mapped_column(sqlalchemy.Boolean)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    camera_id: Mapped[int] = mapped_column(ForeignKey('cameras.id'))
    user: Mapped[User] = relationship("User", back_populates="events")
    notifications: Mapped[list['Notification']] = relationship("Notification", back_populates="event")


class Camera(Base):
    __tablename__ = 'cameras'
    id: Mapped[_id]
    location: Mapped[str] = mapped_column(sqlalchemy.String)
    logs: Mapped[list['Log']] = relationship("Log", back_populates="camera")


class Analytics(Base):
    __tablename__ = 'analytics'
    id: Mapped[_id]
    details: Mapped[str] = mapped_column(sqlalchemy.String)


class Notification(Base):
    __tablename__ = 'notifications'
    id: Mapped[_id]
    message: Mapped[str] = mapped_column(sqlalchemy.String)
    event_id: Mapped[int] = mapped_column(ForeignKey('events.id'))
    event: Mapped[Event] = relationship("Event", back_populates="notifications")


class Log(Base):
    __tablename__ = 'logs'
    id: Mapped[_id]
    data: Mapped[str] = mapped_column(sqlalchemy.String)
    camera_id: Mapped[int] = mapped_column(ForeignKey('cameras.id'))
    camera: Mapped[Camera] = relationship("Camera", back_populates="logs")
