from typing import Annotated
from datetime import date
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship


_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]

Base = declarative_base()


class Book(Base):
    __tablename__ = 'books'

    id: Mapped[_id]
    name: Mapped[str]
    created_at: Mapped[date] = mapped_column(sqlalchemy.DATE, default=date.today())
    author_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('authors.id'))
    author: Mapped['Author'] = relationship(back_populates='book')
    library: Mapped['Library'] = relationship(back_populates='book')


class Author(Base):
    __tablename__ = 'authors'

    id: Mapped[_id]
    name: Mapped[str]
    book_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('books.id'))
    book: Mapped[Book] = relationship(back_populates='author')


class Library(Base):
    __tablename__ = 'library'

    id: Mapped[_id]
    number_of_books: Mapped[int]
    book_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('books.id'))
    book: Mapped[Book] = relationship(back_populates='library')

