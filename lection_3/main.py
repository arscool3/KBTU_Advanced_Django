from pydantic import BaseModel
from fastapi import FastAPI, Depends, Path
from typing import Annotated

app = FastAPI()

literatures = []


class Literature(BaseModel):
    title: str
    author: str


class Book(Literature):
    pass


class Magazine(Literature):
    pass


def add_book_dep(literature: Literature) -> str:
    literatures.append(literature)
    return "{} was added".format(type(literature))


@app.get("/books")
def get_books() -> list:
    return literatures


return_test = tuple[str, list]


@app.post("/book")
def add_book(res: book_dep) -> return_test:
    return res, literatures


@app.post("/magazine")
def add_magazine(res: magazine_dep) -> return_test:
    return res, literatures

# def get_from_db_by_title(book: Book, title: str = Path()) -> Book:
#     books = list(filter(lambda x: x.title == title, literatures))
#     return books[0]
#
# @app.get("/books/{title}")
# def test(
#         book=Depends(get_from_db_by_title)
# ):
#     return book
#
#
# @app.post("/books/{title}/mod/")
# def test(
#         new_author: str,
#         book=Depends(get_from_db_by_title),
#
# ):
#
#     book.author = new_author
#
#     return book
