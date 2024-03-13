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


class Film(Base):
    description: str
    rating: float
    duration: int
    director: Director
    genre: Genre


class CreateFilm(BaseModel):
    name: str

# Movie <-> Genre Many to One
# Movie <-> Director Many to One