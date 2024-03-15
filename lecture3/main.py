from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Annotated

app = FastAPI()
literatures = []


class Book(BaseModel):
    title: str
    author: str


class Magazine(BaseModel):
    title: str
    topic: str




def add_literature_dep(literature: Book | Magazine) -> str:
    literatures.append(literature)
    return "Book added successfully"


@app.post("/books")
def add_book(book_dep: str = Depends(add_literature_dep)) -> str:
    return book_dep


@app.post("/magazines")
def add_magazine(magazine_dep: str = Depends(add_literature_dep)) -> str:
    return magazine_dep