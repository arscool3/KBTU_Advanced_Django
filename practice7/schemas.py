from pydantic import BaseModel

class Base(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class Genre(Base):
    pass

class Director(BaseModel):
    pass

class Base(BaseModel):
    id: int
    name: str

    class Movie(Base):
        description: str
        rating: float
        duration: int
