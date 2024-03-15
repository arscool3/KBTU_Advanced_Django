from pydantic import BaseModel

__all__ = ("Genre", "Director", "Movie", "CreateGenre", "CreateMovie", "CreateDirector")


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


class Movie(Base):
    # description: str
    # rating: int
    # duration: float
    director: Director
    genres: list[Genre]


class CreateMovie(BaseModel):
    name: str
    # description: str
    # rating: int
    # duration: float
    director_id: int


class CreateDirector(BaseModel):
    name: str

# Movie m2o Director
# Movie m2m Genre
