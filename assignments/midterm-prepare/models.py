from typing import Annotated
import sqlalchemy as sq
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.ext.declarative import declarative_base

_id = Annotated[int, mapped_column(sq.Integer, primary_key=True)]

Base = declarative_base()

post_category = sq.Table(
    'post_category', Base.metadata,
    sq.Column('post_id', sq.ForeignKey('t_post.id'), primary_key=True),
    sq.Column('category_id', sq.ForeignKey('t_category.id'), primary_key=True)
)


class User(Base):
    __tablename__ = 't_user'
    id: Mapped[_id]
    username: Mapped[str]
    email: Mapped[str]
    tt: Mapped[str]
    age: Mapped[int]
    password: Mapped[str]
    posts: Mapped[list["Post"]] = relationship("Post", back_populates="author")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="author")


class Post(Base):
    __tablename__ = 't_post'
    id: Mapped[Annotated[int, mapped_column(sq.Integer, primary_key=True)]]
    title: Mapped[str] = mapped_column(sq.String(255))
    content: Mapped[str] = mapped_column(sq.Text)
    user_id: Mapped[Annotated[int, mapped_column(sq.Integer, sq.ForeignKey('t_user.id'))]]
    categories: Mapped[list["Category"]] = relationship(
        "Category",
        secondary="post_category",  # Association table needed for many-to-many
        back_populates="posts",
    )
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="post")
    author: Mapped["User"] = relationship("User", back_populates="posts")


class Comment(Base):
    __tablename__ = 't_comment'
    id: Mapped[Annotated[int, mapped_column(sq.Integer, primary_key=True)]]
    content: Mapped[str] = mapped_column(sq.Text)
    user_id: Mapped[Annotated[int, mapped_column(sq.Integer, sq.ForeignKey('t_user.id'))]]
    post_id: Mapped[Annotated[int, mapped_column(sq.Integer, sq.ForeignKey('t_post.id'))]]
    author: Mapped["User"] = relationship("User", back_populates="comments")
    post: Mapped["Post"] = relationship("Post", back_populates="comments")
    post_id: Mapped[Annotated[int, mapped_column(sq.Integer, sq.ForeignKey('t_post.id'))]]


class Category(Base):
    __tablename__ = 't_category'
    id: Mapped[Annotated[int, mapped_column(sq.Integer, primary_key=True)]]
    name: Mapped[str] = mapped_column(sq.String(255))
    posts: Mapped[list["Post"]] = relationship(
        "Post",
        secondary="post_category",  # Association table needed for many-to-many
        back_populates="categories",
    )
