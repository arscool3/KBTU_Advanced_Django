from typing import Annotated

import sqlalchemy
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship
# from database import Base

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id: Mapped[_id]
    name: Mapped[str]
    age: Mapped[int]

    posts: Mapped[list['Post']] = relationship(back_populates='user')


class Post(Base):
    __tablename__ = 'posts'

    id: Mapped[_id]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    title: Mapped[str]

    user: Mapped[User] = relationship(back_populates="posts")
