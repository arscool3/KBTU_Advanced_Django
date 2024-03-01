from datetime import date
from typing import Union

from pydantic import BaseModel


class BaseBook(BaseModel):
    name: str
    created_at: date

    class Config:
        from_attributes = True


class Book(BaseBook):
    id: int
    author_id: int
    author: Author
    library: Library


class BaseAuthor(BaseModel):
    name: str

    class Config:
        from_attributes = True


class Author(BaseAuthor):
    id: int
    book_id: int
    book: Book


class BaseLibrary(BaseModel):
    number_of_books: int

    class Config:
        from_attributes = True


class Library(BaseLibrary):
    id: int
    book_id: int
    book: Book


ReturnType = Union[Book, Library, Author]