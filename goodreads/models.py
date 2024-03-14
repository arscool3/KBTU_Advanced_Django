#sqlaclhemy models
# 6 Models, 4 relationships(user, book, bookreview, Author, Quote,bookshelf)

from typing import Annotated
import sqlalchemy
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database import Base
from datetime import date

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]

class Goodreads:
    id: Mapped[_id]
    name: Mapped[str]
    description: Mapped[str]

class User(Base, Goodreads):
    __tablename__ = 'users'
    pass

class Book(Base, Goodreads):
    __tablename__ = 'books'
    author_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('authors.id'))
    author: Mapped['Author'] = relationship("Author", back_populates='book')

class Author(Base, Goodreads):
    __tablename__ = 'authors'
    id: Mapped[_id]
    book: Mapped[Book] = relationship("Book", back_populates='author')
 

    """
class Genre(Base):
    __tablename__ = 'genres'
    id: Mapped[_id]
    name = Mapped(str)
    description= Mapped(str)
    book: Mapped['Book'] = relationship(back_populates='books')

class Book(Base):
    __tablename__ = "books"

    id: Mapped[_id]
    name = Mapped(str)
    description = Mapped(str)
#    published_date =  Mapped[date] = mapped_column(sqlalchemy.DATE, default=date.today())
    author = relationship("Author", back_populates="books")
    genre_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('genres.id'))
    genres: Mapped[list[Genre]] = relationship(back_populates='book')



class Author(Base):
    __tablename__ = "authors"

    id: Mapped[_id]
    name = Mapped(str)
    description = Mapped(str)
    books = relationship("Book", back_populates="author")
    quotes=relationship("Quote",back_populates="quotes")

class Quote(Base):
    __tablename__ = "authors"

    id: Mapped[_id]
    name = Mapped(str)
    description = Mapped(str)
#some relationship with author
"""


