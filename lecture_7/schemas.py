from pydantic import BaseModel


class Base(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class Genre(Base):
    pass


class CreateGenre(Genre):
    pass


class Director(Base):
    pass


class CreateDirector(Director):
    pass


class Film(Base):
    description: str
    rating: float
    duration: int
    # todo


class CreateFilm(Film):
    pass

# Movie <-> genre Many to many
# Movie <-> Director Many to one
