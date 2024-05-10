import datetime
from datetime import date
from typing import Annotated, List
import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Column, Integer, Table, func
from database import Base, session

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]


class User(Base):
    __tablename__ = 'users'

    id: Mapped[_id]
    email: Mapped[str]
    password: Mapped[str]
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'), default=1)

    tickets: Mapped[List['Ticket']] = relationship(back_populates='user')
    notifications: Mapped[List['Notification']] = relationship(back_populates='user')
    role: Mapped['Role'] = relationship(back_populates='users')
    events: Mapped[List['Event']] = relationship(back_populates='user')


class Role(Base):
    __tablename__ = 'roles'

    id: Mapped[_id]
    name: Mapped[str] = mapped_column(unique=True)

    users: Mapped[List['User']] = relationship(back_populates='role')


class Event(Base):
    __tablename__ = 'events'

    id: Mapped[_id]
    title: Mapped[str]
    location: Mapped[str]
    start_time: Mapped[date] = mapped_column(sqlalchemy.DateTime, default=datetime.datetime.now())
    end_time: Mapped[date] = mapped_column(sqlalchemy.DateTime, default=datetime.datetime.now())
    organizer_id:  Mapped[int] = mapped_column(ForeignKey('users.id'))
    participants_max: Mapped[int]
    status: Mapped[str] = mapped_column(default='Available')

    @property
    def participants_current(self):
        return session.query(func.count(Ticket.id)).filter(Ticket.event_id == self.id).scalar()

    tickets: Mapped[List['Ticket']] = relationship(back_populates='event')
    user: Mapped['User'] = relationship(back_populates='events')


class Ticket(Base):
    __tablename__ = 'tickets'

    id: Mapped[_id]
    event_id: Mapped[int] = mapped_column(ForeignKey('events.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    status: Mapped[str] = mapped_column(default='Available')  # Available, Reserved, Sold

    event: Mapped['Event'] = relationship(back_populates='tickets')
    user: Mapped['User'] = relationship(back_populates='tickets')


class Notification(Base):
    __tablename__ = 'notifications'

    id: Mapped[_id]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    message: Mapped[str]
    created_at: Mapped[date] = mapped_column(sqlalchemy.DateTime, default=datetime.datetime.now())

    user: Mapped['User'] = relationship(back_populates='notifications')
