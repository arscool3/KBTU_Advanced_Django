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


class CreateDirector(BaseModel):
    name: str


class Director(Base):
    pass


class Movie(Base):
    director: Director
    genres: Genre

class CreateMovie(BaseModel):
    director_id: int
    genre_id: int
    name: str


# Movie -> Genre: Many to Many
# Movie -> Director: Many to One


# Docker: f8938e51653297903976de7ea2ebe566b72bf5f0bc195757c61669fa18467af1
