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


class Film(Base):
    description: str
    rating: float
    duration: int
    director: Director
    genre: Genre


class CreateMovie(BaseModel):
    genre_id: int
    director_id: int
    name: str



class CreateDirector(BaseModel):
    name: str

# Movie <-> Genre Many to One
# Movie <-> Director Many to One
