from pydantic import BaseModel

class Base(BaseModel):

    name: str
    description:str

    class Config:
        from_attributes = True

class User(Base):
    id:int

class CreateUser(Base):
    pass


class Author(Base):
    id:int

class CreateAuthor(Base):
    pass

class Genre(Base):
    id:int

class CreateGenre(Base):
    pass

class Book(Base):
    id:int
    author:Author
    genre:Genre

class CreateBook(Base):
    author_id:int










