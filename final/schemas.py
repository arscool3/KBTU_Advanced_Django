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

from typing import Optional

class Book(Base):
    id: int
    author: Author
    genre: Genre


class CreateBook(Base):
    author_id:int
    genre_id:int

class BaseBookReview(BaseModel):
    review:str
    rating:int

    class Config:
        from_attributes = True  

class BookReview(BaseBookReview):
    id:int
    user:User

class CreateBookReview(BaseBookReview):
    book_id: int
    user_id: int

class BaseQuote(BaseModel):
    description:str

    class Config:
        from_attributes = True  

class Quote(BaseQuote):
    id:int
    author:Author

class CreateQuote(BaseQuote):
    author_id:int







