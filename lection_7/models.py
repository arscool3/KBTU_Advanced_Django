from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from typing import Annotated, Tuple
import sqlalchemy

__all__ = ("Genre", "Director", "Movie")

ModelBase = declarative_base()

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]

movie_genre = sqlalchemy.Table(
    'association_movie_genre',
    ModelBase.metadata,
    sqlalchemy.Column('movie_id', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('movies.id')),
    sqlalchemy.Column('genre_id', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('genres.id'))
)


class BasicModel:
    id: Mapped[_id]
    name: Mapped[str]


class Genre(BasicModel, ModelBase):
    __tablename__ = "genres"
    movies: Mapped[list["Movie"]] = relationship(secondary=movie_genre, back_populates="genres")


class Director(BasicModel, ModelBase):
    __tablename__ = "directors"
    movies: Mapped[list["Movie"]] = relationship(back_populates="director")


class Movie(BasicModel, ModelBase):
    __tablename__ = "movies"
    director_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("directors.id"))
    director: Mapped[Director] = relationship(back_populates="movies")
    genres: Mapped[list[Genre]] = relationship(secondary=movie_genre, back_populates="movies")
