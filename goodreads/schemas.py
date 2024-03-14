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

class CreateAuthor(BaseModel):
    name: str



class Book(Base):
    id:int
    author:Author

class CreateBook(Base):
    author_id:int



# Movie <-> Genre Many to One
# Movie <-> Director Many to One