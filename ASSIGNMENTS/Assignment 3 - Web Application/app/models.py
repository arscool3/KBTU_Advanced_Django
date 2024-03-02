import datetime
from datetime import date
from typing import Annotated

import sqlalchemy
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

from .database import Base

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]
_created_at = Annotated[date, mapped_column(sqlalchemy.DATE, default=datetime.datetime.now())]


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[_id]
    title: Mapped[str]
    content: Mapped[str]
    published: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[_created_at]

    owner_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('users.id'))
    owner: Mapped['User'] = relationship(back_populates='user')


class User(Base):
    __tablename__ = "users"
    id: Mapped[_id]
    email: Mapped[str]
    password: Mapped[str]
    created_at: Mapped[_created_at]
    phone_number: Mapped[str]


class Vote(Base):
    __tablename__ = "votes"
    user_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('users.id'))
    post_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('posts.id'))


class Comment(Base):
    __tablename__ = "comments"
    id: Mapped[_id]
    content: Mapped[str]
    created_at: Mapped[_created_at]
    owner_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('users.id'))
    owner: Mapped['User'] = relationship(back_populates='user')
    post_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('posts.id'))
    post: Mapped['Post'] = relationship(back_populates='post')
