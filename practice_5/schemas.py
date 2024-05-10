from pydantic import BaseModel

class Base(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class Director(Base):
    pass

class Genre(Base):
    pass

class Movie(BaseModel):
    description: str
    rating: float
    duration: int
    director: Director
    genre: Genre
