from typing import Annotated

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapped_column, Mapped, relationship

Base = declarative_base()

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]


class Like(Base):
    __tablename__ = "like"

    id: Mapped[_id]
    user_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("post.id"))

    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")


class User(Base):
    __tablename__ = "user"

    id: Mapped[_id]
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]

    posts = relationship("Post", back_populates="author")
    likes = relationship("Like", back_populates="user")
    comments = relationship("Comment", back_populates="user")


class Post(Base):
    __tablename__ = "post"

    id: Mapped[_id]
    title: Mapped[str]
    content: Mapped[str]
    author_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("user.id"))

    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    likes = relationship("Like", back_populates="post")


class Comment(Base):
    __tablename__ = "comment"

    id: Mapped[_id]
    text: Mapped[str]
    post_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("post.id"))
    user_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("user.id"))

    post = relationship("Post", back_populates="comments")
    user = relationship("User", back_populates="comments")
