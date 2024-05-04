from pydantic import BaseModel


class Base(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class Genre(Base):
    pass


class CreateGenre(BaseModel):
    name: str


class Director(Base):
    pass


class CreateDirector(BaseModel):
    name: str


class Movie(Base):
    director: Director
    genres: Genre


class CreateMovie(BaseModel):
    name: str
    director_id: int
    genre_id: int
