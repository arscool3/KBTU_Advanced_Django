from typing import Annotated
from datetime import date

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship

Base = declarative_base()
_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]

class Author(Base):
    __tablename__ = 'authors'

    id: Mapped[_id]
    name: Mapped[str]
    birth_date: Mapped[date]
    books: Mapped[list['Book']] = relationship('Book', back_populates='author')

class Book(Base):
    __tablename__ = 'books'

    id: Mapped[_id]
    title: Mapped[str]
    publication_date: Mapped[date]
    author_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('authors.id'))
    author: Mapped[Author] = relationship('Author', back_populates='books')
    genre_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('genres.id'))
    genre: Mapped['Genre'] = relationship('Genre', back_populates='books')
    publisher_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('publishers.id'))  # New line
    publisher: Mapped['Publisher'] = relationship('Publisher', back_populates='books')  # New line

class Genre(Base):
    __tablename__ = 'genres'

    id: Mapped[_id]
    name: Mapped[str]
    books: Mapped[list[Book]] = relationship('Book', back_populates='genre')


class Publisher(Base):
    __tablename__ = 'publishers'

    id: Mapped[_id]
    name: Mapped[str]
    books: Mapped[list[Book]] = relationship('Book', back_populates='publisher')
