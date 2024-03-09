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
    description: str
    rating: float
    duration: int
    director: Director
    genre: Genre

# Movie <-> Genre Many to One
# Movie <-> Director Many to One