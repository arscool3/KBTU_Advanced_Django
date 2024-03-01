from __future__ import annotations
from datetime import date
from typing import Union
from abc import abstractmethod
from pydantic import BaseModel
from sqlalchemy.orm import Session
import models as db


class BaseBook(BaseModel):
    name: str
    created_at: date

    class Config:
        from_attributes = True


class CreateBook(BaseBook):
    author_id: int


class BaseAuthor(BaseModel):
    name: str

    class Config:
        from_attributes = True


class CreateAuthor(BaseAuthor):
    pass


class BaseLibrary(BaseModel):
    number_of_books: int

    class Config:
        from_attributes = True


class CreateLibrary(BaseLibrary):
    book_id: int


class BaseReader(BaseModel):
    name: str

    class Config:
        from_attributes = True


class CreateReader(BaseReader):
    book_id: int


class Book(BaseBook):
    id: int
    author_id: int


class Author(BaseAuthor):
    id: int


class Library(BaseLibrary):
    id: int
    book_id: int


class Reader(BaseReader):
    id: int


ReturnType = Union[Book, Library, Author]


class Abs:
    @abstractmethod
    def __init__(self, session: Session):
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> ReturnType:
        raise NotImplementedError()


class BookAbs(Abs):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> Book:
        db_book = self._session.get(db.Book, id)
        return Book.model_validate(db_book)