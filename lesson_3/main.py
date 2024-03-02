from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Annotated

app = FastAPI()

literatures = []
books = []
magazines = []


class Literature(BaseModel):
    title: str
    author: str


class Book(Literature):
    pass


class Magazine(Literature):
    pass


class LiteratureDependency:
    def __init__(self, literature_type: type[Book | Magazine]):
        self.literature_type = literature_type

    def __call__(self, literature: Literature) -> str:
        if self.literature_type == Book:
            books.append(literature)
        else:
            magazines.append(literature)

        return "Literature was added"


book_dep = Annotated[dict[str, type[Book | Magazine]], Depends(LiteratureDependency(Book))]
magazine_dep = Annotated[dict[str, type[Book | Magazine]], Depends(LiteratureDependency(Magazine))]


def add_literature(literature: Book | Magazine) -> str:
    literatures.append(literature)
    return f"{type(literature)} was added"


@app.post('/books')
def add_book(book: book_dep) -> dict[str, type[Book | Magazine]]:
    return book


@app.post('/magazines')
def add_magazine(magazine: magazine_dep) -> dict[str, type[Book | Magazine]]:
    return magazine


@app.get('/books/{book_id}')
def get_book(book_id: int) -> Book:
    return literatures[book_id]
