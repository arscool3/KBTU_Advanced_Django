from typing import Annotated, Optional

import sqlalchemy
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database import Base

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]


class Netflix:
    id: Mapped[_id]
    name: Mapped[str]


class Genre(Netflix, Base):
    __tablename__ = 'genres'
    film: Mapped['Film'] = relationship(back_populates='genres')


class Director(Netflix, Base):
    __tablename__ = 'directors'
    film: Mapped['Film'] = relationship(back_populates='directors')


class Actor(Netflix, Base):
    __tablename__ = 'actors'
    film: Mapped['Film'] = relationship(back_populates='actors')


class User(Netflix, Base):
    __tablename__ = 'users'
    username: Mapped[str]
    email: Mapped[str]
    watchlist: Mapped['Film'] = relationship('Film', secondary='user_watchlist')


class Film(Netflix, Base):
    __tablename__ = 'films'
    title: Mapped[str]
    release_year: Mapped[int]
    director_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('directors.id'))
    genre_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('genres.id'))
    actor_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('actors.id'))
    directors: Mapped[Director] = relationship(back_populates='film')
    genres: Mapped[Genre] = relationship(back_populates='film')
    actors: Mapped[Actor] = relationship(back_populates='film')
    users: Mapped[User] = relationship(back_populates='film')


class UserWatchlist(Base):
    __tablename__ = 'user_watchlist'
    user_id: int = mapped_column(sqlalchemy.ForeignKey('users.id'), primary_key=True)
    film_id: int = mapped_column(sqlalchemy.ForeignKey('films.id'), primary_key=True)
    added_at: sqlalchemy.DateTime = mapped_column(sqlalchemy.DateTime, default=sqlalchemy.func.now())
    user: Mapped[User] = relationship(User, back_populates="watchlist")
    film: Mapped[Film] = relationship(Film, back_populates="users")

