from typing import List, Optional

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


class Journal(BaseModel):
    id: int
    method: str
    request: str
    data: Optional[dict]
    created_at: str

    class Config:
        from_attributes = True


class JournalMessage(BaseModel):
    method: str
    request: str
    data: Optional[dict]

    class Config:
        from_attributes = True


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
