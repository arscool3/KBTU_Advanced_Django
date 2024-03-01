from abc import abstractmethod

from pydantic import BaseModel
from sqlalchemy.orm import Session

import models as db
from schemas import Author, Book, Genre, Publisher

class AbcRepository:
    @abstractmethod
    def __init__(self, session: Session):
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Author | Book | Publisher | Genre:
        raise NotImplementedError

class AuthorRepository(AbcRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> Author:
        db_author = self._session.get(db.Author, id)
        if db_author is None:
            return "No such author!"
        return Author.model_validate(db_author)

class BookRepository(AbcRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> Book:
        db_book = self._session.get(db.Book, id)
        if db_book is None:
            return "No such book!"
        return Book.model_validate(db_book)

class GenreRepository(AbcRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> Genre:
        db_genre = self._session.get(db.Genre, id)
        if db_genre is None:
            return "No such genre!"
        return Genre.model_validate(db_genre)

class PublisherRepository(AbcRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> Publisher:
        db_publisher = self._session.get(db.Publisher, id)
        if db_publisher is None:
            return "No such publisher!"
        return Publisher.model_validate(db_publisher)
