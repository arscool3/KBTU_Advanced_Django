from typing import Annotated, List
import sqlalchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from datetime import datetime

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]


class User(Base):
    __tablename__ = 'users'

    id: Mapped[_id]
    name: Mapped[str]
    age: Mapped[int]

    posts: Mapped[List['Post']] = relationship(back_populates='user')
    comments: Mapped[List['Comment']] = relationship(back_populates='user')
    # follows: Mapped[List['Follow']] = relationship(back_populates='follows')


class Post(Base):
    __tablename__ = 'posts'

    id: Mapped[_id]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    title: Mapped[str]
    published_at: Mapped[datetime] = mapped_column(sqlalchemy.DateTime, default=datetime.now())

    user: Mapped[User] = relationship(back_populates="posts")
    comments: Mapped[List['Comment']] = relationship(back_populates='post')


class Comment(Base):
    __tablename__ = 'comments'

    id: Mapped[_id]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'))
    text: Mapped[str]
    published_at: Mapped[datetime] = mapped_column(sqlalchemy.DateTime, default=datetime.now())

    user: Mapped[User] = relationship(back_populates="comments")
    post: Mapped[Post] = relationship(back_populates="comments")


# class Follow(Base):
#     __tablename__ = 'follows'
#
#     follower_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
#     following_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
