from fastapi import FastAPI, Depends
from sqlalchemy import select
import models as db
from typing import Union, Type, List
from database import get_db
from schemas import *
import punq

app = FastAPI()


def get_book_list(dbb: Session = Depends(get_db)):
    db_books = dbb.execute(select(db.Book)).scalars().all()
    books = []
    for db_book in db_books:
        books.append(Book.model_validate(db_book))
    return books


@app.get("/books")
def get_books(books: List[Book] = Depends(get_book_list)) -> List[Book]:
    return books


@app.get("/readers")
def get_reader(dbb: Session = Depends(get_db)):
    db_readers = dbb.execute(select(db.Reader)).scalars().all()
    readers = []
    for db_reader in db_readers:
        readers.append(Reader.model_validate(db_reader))
    return readers


@app.get("/authors")
def get_authors(dbb: Session = Depends(get_db)):
    db_authors = dbb.execute(select(db.Author)).scalars().all()
    authors = []
    for db_author in db_authors:
        authors.append(Author.model_validate(db_author))
    return authors


@app.get("/library")
def view_library(dbb: Session = Depends(get_db)):
    db_library = dbb.execute(select(db.Library)).scalars().all()
    library = []
    for item in db_library:
        library.append(Library.model_validate(item))
    return library


@app.post("/books")
def add_books(book: CreateBook, dbb: Session = Depends(get_db)) -> str:
    dbb.add(db.Book(**book.model_dump()))
    dbb.commit()
    dbb.close()
    return "Added"


@app.post("/readers")
def add_readers(reader: CreateReader, dbb: Session = Depends(get_db)) -> str:
    dbb.add(db.Reader(**reader.model_dump()))
    dbb.commit()
    dbb.close()
    return "Added"


@app.post("/author")
def add_author(author: CreateAuthor, dbb: Session = Depends(get_db)):
    dbb.add(db.Author(**author.model_dump()))
    dbb.commit()
    dbb.close()
    return "Added"


@app.post("/library")
def add_library(library: CreateLibrary, dbb: Session = Depends(get_db)):
    dbb.add(db.Library(**library.model_dump()))
    dbb.commit()
    dbb.close()
    return "Added"


class ByIdDep:
    def __init__(self, abc: Abs):
        self.abc = abc

    def __call__(self, id: int) -> ReturnType:
        return self.abc.get_by_id(id)


def get_container(repository: type[Abs], dbb: Session = Depends(get_db)) -> punq.Container:
    container = punq.Container()
    container.register(Abs, repository, instance=repository(session=dbb))
    container.register(ByIdDep)
    return container


app.add_api_route("/books/{id}", get_container(BookAbs).resolve(ByIdDep), methods=["GET"])

