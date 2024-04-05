from pydantic import BaseModel


class FilmBase(BaseModel):
    name: str
    director: str


class Film(FilmBase):
    id: int


class CreateFilm(FilmBase):
    pass