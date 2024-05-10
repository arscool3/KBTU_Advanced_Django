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
    directors: Director
    genres: Genre


class CreateFilm(BaseModel):
    director_id: int
    genre_id: int
    name: str

# Movie <-> Genre Many to One
# Movie <-> Director Many to One
