from __future__ import annotations

from typing import Annotated, Callable

import punq
from pydantic import BaseModel
from fastapi import FastAPI, Depends

app = FastAPI()

books = []
magazines = []


class Magazine(BaseModel):
    title: str
    content: str
    desc: str


class Fashion(Magazine):
    pass


class Sport(Magazine):
    pass


class Business(Magazine):
    pass


fashions = []
sports = []
business = []


class Literature(BaseModel):
    title: str
    author: str


class Book(Literature):
    pass


class Magazine(Literature):
    pass


# class LiteratureDependency:
#     def __init__(self, literature_type: type[Book] | type[Magazine]):
#         self.literature_type = literature_type
#
#     def __call__(self, literature: Literature) -> str:
#         if self.literature_type == Book:
#             books.append(literature)
#         else:
#             magazines.append(literature)
#         return "Literature was added"


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

# @app.get('/magazines')
# def get_magazines() -> list[Magazine]:
#     return magazine_dep

# CREATE 3 VIEWS WITH DEPENDECY INJECTION
# 2 WITH FUNCTION DEPENDENCY INJECTION
# 1 WITH INSTANCE OF CLASS AS CALLABLE DI

#
# class Stub:
#     def __init__(self, dependency: Callable, **kwargs):
#         self._dependency = dependency
#         self._kwargs = kwargs
#
#     def __call__(self):
#         raise NotImplementedError
#
#     def __eq__(self, other) -> bool:
#         if isinstance(other, Stub):
#             return (
#                     self._dependency == other._dependency
#                     and self._kwargs == other._kwargs
#             )
#         else:
#             if not self._kwargs:
#                 return self._dependency == other
#             return False
#
#     def __hash__(self):
#         if not self._kwargs:
#             return hash(self._dependency)
#         serial = (
#             self._dependency,
#             *self._kwargs.items(),
#         )
#         return hash(serial)
#
#
# class Repo:
#     def __init__(self, a: int):
#         self.a = a
#
#
# @app.get("/")
# async def root(repo: Repo = Depends(Stub(Repo))) -> int:
#     return repo.a
#
#
# @app.get("/1")
# async def root(repo: Repo = Depends(Stub(Repo, key="1"))) -> int:
#     return repo.a
#
#
# app.dependency_overrides[Repo] = lambda: Repo(0)
# app.dependency_overrides[Stub(Repo, key="1")] = lambda: Repo(1)
