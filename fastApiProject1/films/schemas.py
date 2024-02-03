from pydantic import BaseModel


class Film(BaseModel):
    id: int
    name: str
    rating: int
    director: str


class AddFilm(BaseModel):
    name: str
    rating: int
    director: str

