import datetime
from typing import List

from pydantic import BaseModel


class BaseUser(BaseModel):
    name: str
    email: str

    class Config:
        from_attributes = True


class User(BaseUser):
    id: int


class CreateUser(BaseUser):
    pass


class BaseAuthor(BaseModel):
    first_name: str
    last_name: str

    class Config:
        from_attributes = True


class Author(BaseAuthor):
    id: int


class CreateAuthor(BaseAuthor):
    pass


class BaseBookCategory(BaseModel):
    name: str
    description: str

    class Config:
        from_attributes = True


class CreateBookCategory(BaseBookCategory):
    pass


class BookCategory(BaseBookCategory):
    id: int


class BaseBook(BaseModel):
    title: str
    description: str
    published_at: datetime.date

    class Config:
        from_attributes = True


class CreateBook(BaseBook):
    author_id: int
    category_id: int


class Book(BaseBook):
    author: Author
    category: BookCategory
