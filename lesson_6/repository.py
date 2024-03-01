from abc import abstractmethod
from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

import schemas
import models


class AbcRepository:

    @abstractmethod
    def get_all(self):
        raise NotImplementedError()


class UserRepository(AbcRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        instances = self.session.execute(select(models.User)).scalars().all()
        return [schemas.User.model_validate(user) for user in instances]


class AuthorRepository(AbcRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        instances = self.session.execute(select(models.BookAuthor)).scalars().all()
        return [schemas.Author.model_validate(author) for author in instances]


class BookCategoryRepository(AbcRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        instances = self.session.execute(select(models.BookCategory)).scalars().all()
        return [schemas.BookCategory.model_validate(book_category) for book_category in instances]


class BookRepository(AbcRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        instances = self.session.execute(select(models.Book)).scalars().all()
        return [schemas.Book.model_validate(book) for book in instances]
