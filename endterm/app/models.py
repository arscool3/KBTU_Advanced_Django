from typing import Annotated
from datetime import date, datetime
import sqlalchemy
from sqlalchemy import Table, Column, Integer, ForeignKey, JSON, func

from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.database import Base

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]


class GeneralInfo:
    id: Mapped[_id]
    name: Mapped[str]
    created_at: Mapped[date] = mapped_column(sqlalchemy.DATE, default=date.today())


movie_actor = Table(
    'movie_actor',
    Base.metadata,
    Column('movies_id', Integer, ForeignKey('movies.id')),
    Column('actors_id', Integer, ForeignKey('actors.id'))
)


class Actor(GeneralInfo, Base):
    __tablename__ = 'actors'
    movies: Mapped[list['Movie']] = relationship('Movie', secondary=movie_actor, back_populates='actors')


class Genre(GeneralInfo, Base):
    __tablename__ = 'genres'
    id: Mapped[_id]
    movie: Mapped['Movie'] = relationship(back_populates='genre')


class Studio(GeneralInfo, Base):
    __tablename__ = 'studios'
    movie: Mapped['Movie'] = relationship(back_populates='studio')


class Director(GeneralInfo, Base):
    __tablename__ = 'directors'
    movie: Mapped['Movie'] = relationship(back_populates='director')


class Movie(Base, GeneralInfo):
    __tablename__ = 'movies'
    rating: Mapped[float]
    director_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('directors.id'))
    genre_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('genres.id'))
    studio_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('studios.id'))
    director: Mapped[Director] = relationship(back_populates='movie')
    genre: Mapped[Genre] = relationship(back_populates='movie')
    studio: Mapped['Studio'] = relationship(back_populates='movie')
    actors: Mapped[list[Actor]] = relationship('Actor', secondary=movie_actor, back_populates='movies')


class AccessLogJournal(Base):
    __tablename__ = 'access_log_journal'
    id: Mapped[_id]
    data = Column(JSON, nullable=True)
    method: Mapped[str]
    request: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

