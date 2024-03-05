from pydantic import BaseModel


class GenreBase(BaseModel):
    name: str

    class Config:
        from_attributes = True


class DirectorBase(BaseModel):
    name: str

    class Config:
        from_attributes = True


class Genre(GenreBase):
    id: int


class Director(DirectorBase):
    id: int


class FilmBase(BaseModel):
    name: str
    description: str
    rating: float
    duration: int

    class Config:
        from_attributes = True


class Film(FilmBase):
    id: int
    genres: Genre
    directors: Director


class CreateGenre(GenreBase):
    pass


class CreateDirector(DirectorBase):
    pass


class CreateFilm(FilmBase):
    genre_id: int
    director_id: int