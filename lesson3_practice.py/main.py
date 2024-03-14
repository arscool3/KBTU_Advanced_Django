from typing import Annotated, Callable

import punq
from pydantic import BaseModel
from fastapi import FastAPI, Depends

app = FastAPI()

books = []
magazines = []


class Literature(BaseModel):
    title: str
    author: str


class Book(Literature):
    pass


class Magazine(Literature):
    pass




class LiteratureSubLayer:
    def __init__(self, log_message: str):
        self.log_message = log_message

    def add_literature(self, literature: Book | Magazine):
        print(self.log_message)
        books.append(literature) if isinstance(literature, Book) else magazines.append(literature)


class LiteratureMainLayer:
    def __init__(self, repo: LiteratureSubLayer):
        self.repo = repo

    def add_literature(self, literature: Book | Magazine):
        print("SOME LOGGING")
        self.repo.add_literature(literature)
        print("END LOGGING")

        return "literature was added"

    def add_book(self, book: Book) -> str:
        return self.add_literature(book)

    def add_magazine(self, magazine: Magazine) -> str:
        return self.add_literature(magazine)

def get_container() -> punq.Container:
    container = punq.Container()
    container.register(LiteratureSubLayer, instance=LiteratureSubLayer(log_message='I AM INSIDE SUB LAYER'))
    container.register(LiteratureMainLayer)
    return container


@app.post('/books')
def add_book(book: Annotated[str, Depends(get_container().resolve(LiteratureMainLayer).add_book)]) -> str:
    return book


@app.post('/magazines')
def add_magazine(magazine: Annotated[str, Depends(get_container().resolve(LiteratureMainLayer).add_book)]) -> str:
    return magazine

@app.get('/books')
def get_books() -> list[Book]:
    return books

