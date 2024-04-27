from fastapi import FastAPI, Depends
from pydantic import BaseModel


app = FastAPI()

books = []


class Book(BaseModel):
    title: str
    author: str


class Magazine(BaseModel):
    title: str
    author: str


def add_book_dep(literature: Book | Magazine)-> str:
    books.append(literature)
    return f"{literature} was added"


@app.post('/books')
def add_book(book_dep: str=Depends(add_book_dep))-> str:
    return book_dep