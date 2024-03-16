import datetime
from typing import Annotated

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapped_column, Mapped, relationship

Base = declarative_base()

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]


class User(Base):
    __tablename__ = "users"

    id: Mapped[_id]
    name: Mapped[str]
    email: Mapped[str]


class BookAuthor(Base):
    __tablename__ = "book_authors"

    id: Mapped[_id]
    first_name: Mapped[str]
    last_name: Mapped[str]

    books = relationship("Book", back_populates="author")


class BookCategory(Base):
    __tablename__ = "book_categories"

    id: Mapped[_id]
    name: Mapped[str]
    description: Mapped[str]

    books = relationship("Book", back_populates="category")


class Book(Base):
    __tablename__ = "books"

    id: Mapped[_id]
    title: Mapped[str]
    description: Mapped[str]
    published_at: Mapped[datetime.date]
    author_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("book_authors.id"))
    category_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("book_categories.id"))

    author = relationship("BookAuthor", back_populates="books")
    category = relationship("BookCategory", back_populates="books")
