
import punq
from fastapi import FastAPI, Depends
from typing import Annotated
from pydantic import BaseModel

app = FastAPI()

books = []
magazines = []


class Literature(BaseModel):
    title: str
    author: str


class Magazine(Literature):
    pass


class Book(Literature):
    pass

# class LiteratureDependency:
#     def __init__(self, literature_type: type[Book] | type[Magazine]):
#         self.literature_type = literature_type
#
#     def __call__(self, literature: Book | Magazine):
#         if self.literature_type == Book:
#             return books.append(literature)
#         else:
#             return magazines.append(literature)
#
#
# book_dep = Annotated[str, Depends(LiteratureDependency(Book))]
# magazine_dep = Annotated[str, Depends(LiteratureDependency(Magazine))]


class LiteratureSubLayer:
    def __init__(self, log_message: str):
        self.log_message = log_message

    def add_literature(self, literature: Book | Magazine):
        books.append(literature) if isinstance(literature, Book) else magazines.append(literature)


class LiteratureMainLayer:
    def __init__(self, repo: LiteratureSubLayer):
        self.repo = repo

    def add_literature(self, literature: Book | Magazine):
        self.repo.add_literature(literature)
        return "Literature was added"

    def add_book(self, book: Book) -> str:
        return self.add_literature(book)

    def add_magazine(self, magazine: Magazine) -> str:
        return self.add_literature(magazine)


def get_container() -> punq.Container:
    container = punq.Container()
    container.register(LiteratureSubLayer, instance=LiteratureSubLayer(log_message="Sub layer"))
    container.register(LiteratureMainLayer)
    return container


@app.post('/books')
def add_books(book: Annotated[str, Depends(get_container().resolve(LiteratureMainLayer).add_book)]):
    return book


@app.get('/books')
def get_books() -> list[Book]:
    return books


@app.post('/magazines')
def add_magazine(magazine: Annotated[str, Depends(get_container().resolve(LiteratureMainLayer).add_magazine)]):
    return magazine


@app.get('/magazines')
def get_magazines() -> list[Magazine]:
    return magazines
