import punq
from fastapi import FastAPI
from sqlalchemy import select

import models as db
from database import session
from schemas import Book, Library, Author
app = FastAPI()


class Dependency:
   pass


@app.get("/books")
def get_books():
    db_books = session.execute(select(db.Book)).scalars().all()
    books = []
    for db_book in db_books:
        books.append(Book.model_validate(db_book))
    return books


@app.get("/authors")
def get_authors():
    db_authors = session.execute(select(db.Author)).scalars().all()
    authors = []
    for db_author in db_authors:
        authors.append(Author.model_validate(db_author))
    return authors


@app.get("/library")
def view_library():
    db_library = session.execute(select(db.Library)).scalars().all()
    library = []
    for item in db_library:
        library.append(Author.model_validate(item))
    return library


@app.post("/books")
def add_books(book: CreateBook) -> str:
    session.add(db.Book(**book.model_dump()))
    session.commit()
    session.close()
    return "Added"


@app.post("/author")
def add_country(author: CreateAuthor):
    session.add(db.Author(**author.model_dump()))
    session.commit()
    session.close()
    return "Added"


@app.post("/library")
def add_president(library: AddBookToLib):
    session.add(db.Library(**library.model_dump()))
    session.commit()
    session.close()
    return "Added"