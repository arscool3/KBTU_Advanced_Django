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
    description: str
    rating: int
    duration: int
    director_id: int
    genre_id: int

    class Config:
        orm_mode = True

class CreateMovie(BaseModel):
    name: str
    description: str
    rating: float
    duration: int
    director_id: int
    genre_id: int
