from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

import models
from main import get_db
class Database:
    def __call__(self) -> Session:
        return get_db()

def get_user_model(user_id: int, db: Database) -> models.User | None:
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    return db_user

def get_genre_model(genre_id: int, db: Database) -> models.Genre | None:
    db_genre = db.query(models.Genre).filter(models.Genre.id == genre_id).first()
    return db_genre

def get_book_model(book_id: int, db: Database) -> models.Book | None:
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    return db_book

def get_quote_model(quote_id: int, db: Database) -> models.Quote | None:
    db_quote = db.query(models.Quote).filter(models.Quote.id == quote_id).first()
    return db_quote

class UserDependencyClass:
    def __call__(self, db_user: models.User = Depends(get_user_model)) -> models.User | None:
        return db_user

class GenreDependencyClass:
    def __call__(self, db_genre: models.Genre = Depends(get_genre_model)) -> models.Genre | None:
        return db_genre

class BookDependencyClass:
    def __call__(self, db_book: models.Book = Depends(get_book_model)) -> models.Book | None:
        return db_book

class QuoteDependencyClass:
    def __call__(self, db_quote: models.Quote = Depends(get_quote_model)) -> models.Quote | None:
        return db_quote

UserDependency = Annotated[models.User, Depends(UserDependencyClass())]
GenreDependency = Annotated[models.Genre, Depends(GenreDependencyClass())]
BookDependency = Annotated[models.Book, Depends(BookDependencyClass())]
QuoteDependency = Annotated[models.Quote, Depends(QuoteDependencyClass())]

ModelUserDependency = Annotated[models.User, Depends(get_user_model)]
ModelGenreDependency = Annotated[models.Genre, Depends(get_genre_model)]
ModelBookDependency = Annotated[models.Book, Depends(get_book_model)]
ModelQuoteDependency = Annotated[models.Quote, Depends(get_quote_model)]
