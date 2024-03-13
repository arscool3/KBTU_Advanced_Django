from typing import Annotated

import `sqlalchemy`
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database import Base

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]


class Cinema:
    id: Mapped[_id]
    name: Mapped[str]


class Genre(Cinema, Base):
    tablename = 'genres'
    film: Mapped[list('Film')] = relationship(back_populates='genres')


class Director(Cinema, Base):
    tablename = 'directors'
    film: Mapped[list('Film')] = relationship(back_populates='directors')


class Film(Cinema, Base):
    tablename = 'films'
    director_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('directors.id'))
    genre_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('genres.id'))
    director: Mapped[Director] = relationship(back_populates='film')
    genre: Mapped[Genre] = relationship(back_populates='film')