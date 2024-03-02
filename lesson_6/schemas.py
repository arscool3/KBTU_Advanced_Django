from datetime import date
from pydantic import BaseModel


class BaseDirector(BaseModel):
    name: str

    class Config:
        from_attributes = True


class Director(BaseDirector):
    id: int


class CreateDirector(BaseDirector):
    pass


class BaseGenre(BaseModel):
    name: str

    class Config:
        from_attributes = True


class Genre(BaseGenre):
    id: int


class CreateGenre(BaseGenre):
    pass


class BaseStudio(BaseModel):
    name: str

    class Config:
        from_attributes = True


class Studio(BaseStudio):
    id: int


class CreateStudio(BaseStudio):
    pass


class BaseMovie(BaseModel):
    title: str
    release_date: date

    class Config:
        from_attributes = True


class Movie(BaseMovie):
    id: int
    director: Director
    genre: Genre
    studio: Studio


class CreateMovie(BaseMovie):
    director_id: int
    genre_id: int
    studio_id: int


ReturnType = Movie, Director, Genre, Studio
