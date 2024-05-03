from datetime import datetime
from typing import Annotated

import sqlalchemy
from sqlalchemy import create_engine, Column, ForeignKey, Integer, DateTime
from sqlalchemy.orm import Session, declarative_base, mapped_column, Mapped, relationship

url = 'postgresql://postgres:postgres@localhost:5440/postgres'
engine = create_engine(url)
session = Session(engine)

Base = declarative_base()


_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]


class User(Base):
    __tablename__ = "users"

    id: Mapped[_id]
    username: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    chats: Mapped[relationship] = relationship("Chat", back_populates="owner")
    groups: Mapped[relationship] = relationship("Group", back_populates="owner")


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[_id]
    name: Mapped[str]
    owner_id: Mapped[int] = Column(Integer, ForeignKey("users.id"))
    owner: Mapped[relationship] = relationship("User", back_populates="chats")
    messages: Mapped[relationship] = relationship("Message", back_populates="chat")


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[_id]
    content: Mapped[str]
    sender_id: Mapped[int] = Column(Integer, ForeignKey("users.id"))
    chat_id: Mapped[int] = Column(Integer, ForeignKey("chats.id"))
    sent_at: Annotated[datetime, Column] = Column(DateTime, default=datetime.utcnow)
    received_at: Annotated[datetime, Column] = Column(DateTime, default=None)
    chat: Mapped[relationship] = relationship("Chat", back_populates="messages")
    attachments: Mapped[relationship] = relationship("Attachment", uselist=True, back_populates="message")
    notifications: Mapped[relationship] = relationship("Notification", back_populates="message")


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[_id]
    name: Mapped[str]
    owner_id: Mapped[int] = Column(Integer, ForeignKey("users.id"))
    owner: Mapped[relationship] = relationship("User", back_populates="groups")
    memberships: Mapped[relationship] = relationship("Membership", back_populates="group")


class Membership(Base):
    __tablename__ = "memberships"

    id: Mapped[_id]
    user_id: Mapped[int] = Column(Integer, ForeignKey("users.id"))
    group_id: Mapped[int] = Column(Integer, ForeignKey("groups.id"))
    group: Mapped[relationship] = relationship("Group", back_populates="memberships")


class Attachment(Base):
    __tablename__ = "attachments"

    id: Mapped[_id]
    filename: Mapped[str]
    message_id: Mapped[int] = Column(Integer, ForeignKey("messages.id"))
    message: Mapped[relationship] = relationship("Message", back_populates="attachments")


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[_id]
    name: Mapped[str]
    message_id: Mapped[int] = Column(Integer, ForeignKey("messages.id"))
    message: Mapped[relationship] = relationship("Message", back_populates="notifications")


# Docker: c9314cc1492761b004e57e1102f555d04237e361c9686d1d8ec788645a6a40d1
