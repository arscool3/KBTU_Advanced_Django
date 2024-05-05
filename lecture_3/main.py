from typing import Annotated

from fastapi import FastAPI, Depends
from pydantic import BaseModel

app = FastAPI()

literatures = []


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

    def __call__(self, literature: Literature):
        return {'type': self.literature_type}


book_dep = Annotated[dict, Depends(LiteratureDependency(Book))]
magazine_dep = Annotated[dict, Depends(LiteratureDependency(Magazine))]


def add_literature_dep(literature: Book | Magazine) -> str:
    literatures.append(literature)
    return f'Added {type(literature).__name__}'


@app.post("/books")
def add_book(book_dep: str = Depends(add_literature_dep)) -> str:
    return book_dep


@app.post("/magazines")
def add_magazine(magazine_dep: str = Depends(add_literature_dep)) -> str:
    return magazine_dep


@app.get("/literatures")
def get_literatures() -> list:
    return literatures
