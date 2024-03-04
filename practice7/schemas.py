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


class Movie(Base):
    director_id: int
    genre_id: int

class CreateMovie(BaseModel):
    name: str
    director_id: int
    genre_id: int
   


# Movie <-> Genre Many to One
# Movie <-> Director Many to One