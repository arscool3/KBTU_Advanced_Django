from typing import List

from pydantic import BaseModel

from app.models import Actor


class Base(BaseModel):
    name: str

    class Config:
        from_attributes = True


class Genre(Base):
    pass


class CreateGenre(Base):
    pass


class Studio(Base):
    pass


class Director(Base):
    pass


class Movie(Base):
    director: Director
    genre: Genre
    studio: Studio
    rating: float
    actors: List[int]


class CreateMovie(BaseModel):
    name: str
    director_id: int
    genre_id: int
    studio_id: int
    rating: float
