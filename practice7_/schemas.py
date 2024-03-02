from pydantic import BaseModel

"""
class Director(Cinema, Base):
    __tablename__ = 'directors'
    film: Mapped['Film'] = relationship(back_populates='directors')

"""
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
    name:str


class Movie(Base):
    description: str
    rating: float
    duration: int
    director: Director
    genre: Genre
class CreateMovie(BaseModel):
    name:str
    description: str
    rating: float
    duration: int
    director_id: int
    genre_id: int


# Movie <-> Genre Many to One
# Movie <-> Director Many to One