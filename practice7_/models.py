from typing import Annotated

import sqlalchemy
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database import Base

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]


class Cinema:
    id: Mapped[_id]
    name: Mapped[str]


class Genre(Cinema, Base):
    __tablename__ = 'genres'
    movie: Mapped['Movie'] = relationship(back_populates='genres')


class Director(Cinema, Base):
    __tablename__ = 'directors'
    movie: Mapped['Movie'] = relationship(back_populates='directors')


class Movie(Cinema, Base):
    __tablename__ = 'movies'
    description:Mapped[str]
    rating:Mapped[int]
    duration:Mapped[int]
    director_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('directors.id'))
    genre_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('genres.id'))
    directors: Mapped[list[Director]] = relationship(back_populates='movie')
    genres: Mapped[list[Genre]] = relationship(back_populates='movie')
