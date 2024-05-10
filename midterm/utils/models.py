from typing import Annotated, List

import jwt
import sqlalchemy
from sqlalchemy.orm import mapped_column, Mapped, relationship

from utils.database import Base

_id = Annotated[int, mapped_column(sqlalchemy.INTEGER, primary_key=True)]
secret_key = "advanced django alga"


class User(Base):
    __tablename__ = "users"
    id: Mapped[_id]
    name: Mapped[str]
    surname: Mapped[str]
    username: Mapped[str]
    password: Mapped[str]
    posts: Mapped['Post'] = relationship("Post", back_populates="user")
    comments: Mapped['Comment'] = relationship("Comment", back_populates="user")
    complaints: Mapped['Complaint'] = relationship("Complaint", back_populates="user")
    likes: Mapped['Like'] = relationship("Like", back_populates="user")

    def generate_token(self) -> dict:
        payload = {
            "id": self.id,
        }
        access_token = jwt.encode(payload, secret_key)
        return {"access_token": access_token}

    def validate_password(self, password: str) -> bool:
        return self.password == password


class Post(Base):
    __tablename__ = "posts"
    id: Mapped[_id]
    title: Mapped[str]
    description: Mapped[str]
    user_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('users.id'))
    user: Mapped[User] = relationship(User, back_populates="posts")
    comments: Mapped['Comment'] = relationship("Comment", back_populates="post")
    complaints: Mapped['Complaint'] = relationship("Complaint", back_populates="post")
    likes: Mapped['Like'] = relationship("Like", back_populates="post")


class Comment(Base):
    __tablename__ = "comments"
    id: Mapped[_id]
    description: Mapped[str]
    user_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('users.id'))
    user: Mapped[User] = relationship(User, back_populates="comments")
    post_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('posts.id'))
    post: Mapped[Post] = relationship(Post, back_populates="comments")


class Complaint(Base):
    __tablename__ = "complaints"
    id: Mapped[_id]
    description: Mapped[str]
    user_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('users.id'))
    user: Mapped[User] = relationship(User, back_populates="complaints")
    post_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('posts.id'))
    post: Mapped[Post] = relationship(Post, back_populates="complaints")


class Like(Base):
    __tablename__ = "likes"
    id: Mapped[_id]
    user_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('users.id'))
    user: Mapped[User] = relationship(User, back_populates="likes")
    post_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('posts.id'))
    post: Mapped[Post] = relationship(Post, back_populates="likes")


class Admin(Base):
    __tablename__ = "admins"
    id: Mapped[_id]
    name: Mapped[str]
    surname: Mapped[str]
    username: Mapped[str]
    password: Mapped[str]



