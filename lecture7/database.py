from typing import Annotated, List

import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import Session, declarative_base, mapped_column, Mapped, relationship

url = 'postgresql://postgres:postgres@localhost:5435/postgres'
engine = create_engine(url)
session = Session(engine)

Base = declarative_base()


_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]

class Cinema:
    id: Mapped[_id]
    name: Mapped[str]


class Genre(Cinema, Base):
    __tablename__ = 'genres'
    film: Mapped['Film'] = relationship(back_populates='genres')


class Director(Cinema, Base):
    __tablename__ = 'directors'
    films: Mapped['Film'] = relationship(back_populates='director')


class Film(Cinema, Base):
    __tablename__ = 'films'
    director_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('directors.id'))
    genre_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('genres.id'))
    director: Mapped[list[Director]] = relationship(back_populates='films')
    genres: Mapped[list[Genre]] = relationship(back_populates='film')