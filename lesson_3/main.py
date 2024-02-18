from __future__ import annotations
from typing import Annotated
from dataclasses import dataclass
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


class LiteratureDependency:
    def __init__(self, literature_type: type[Book] | type[Magazine]):
        self.literature_type = literature_type

    def __call__(self, literature: Literature) -> str:
        if self.literature_type == Book:
            books.append(literature)
        else:
            magazines.append(literature)

        return "Literature was added"


book_dep = Annotated[str, Depends(LiteratureDependency(Book))]
mag_dep = Annotated[str, Depends(LiteratureDependency(Magazine))]


@app.post("/books")
def add_book(literature_dep: str = Depends(book_dep)) -> str:
    return literature_dep


@app.post("/magazines")
def add_magazine(literature_dep: str = Depends(mag_dep)) -> str:
    return literature_dep


