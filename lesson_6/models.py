from typing import Annotated
from datetime import date

import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]


class Director(Base):
    __tablename__ = 'directors'

    id: Mapped[_id]
    name: Mapped[str]

    movie: Mapped['Movie'] = relationship(back_populates='director')


class Genre(Base):
    __tablename__ = 'genres'

    id: Mapped[_id]
    name: Mapped[str]

    movie: Mapped['Movie'] = relationship(back_populates='genre')


class Studio(Base):
    __tablename__ = 'studios'

    id: Mapped[_id]
    name: Mapped[str]

    movie: Mapped['Movie'] = relationship(back_populates='studio')


class Movie(Base):
    __tablename__ = 'movies'

    id: Mapped[_id]
    title: Mapped[str]
    release_date: Mapped[date]
    rating: Mapped[int]

    director_id = mapped_column(sqlalchemy.ForeignKey('directors.id'))
    genre_id = mapped_column(sqlalchemy.ForeignKey('genres.id'))
    studio_id = mapped_column(sqlalchemy.ForeignKey('studios.id'))

    director: Mapped['Director'] = relationship(back_populates='movie')
    genre: Mapped['Genre'] = relationship(back_populates='movie')
    studio: Mapped['Studio'] = relationship(back_populates='movie')
