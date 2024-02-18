from fastapi import FastAPI, Query, Depends
from pydantic import BaseModel, Field

app = FastAPI()

books = []


class Book(BaseModel):
    title: str = Field(max_length=100)
    author: str = Field(max_length=50)


def get_book_list() -> list[Book]:
    return books


def get_book_by_id(id: int) -> Book:
    if 0 <= id < len(books):
        return books[id]
    else:
        return "Book was ot found"


def add_book(book: Book) -> str:
    books.append(book)
    return "Book was added"


def get_books_by_author(author: str = Query(...)) -> list[Book]:
    return [book for book in books if book.author.lower() == author.lower()]


@app.get("/books")
def get_books(books: list[Book] = Depends(get_book_list)) -> list[Book]:
    return books


@app.get("/books/{id}")
def get_book_by_id_view(id: int) -> Book:
    return get_book_by_id(id)


@app.post("/books")
def add_book_view(book: Book) -> str:
    return add_book(book)


@app.get("/books_by_author/")
def get_books_by_author_view(books: list[Book] = Depends(get_books_by_author)) -> list[Book]:
    return books


class BookListDep:
    def __call__(self) -> list[Book]:
        return books


book_list_dep = BookListDep()


@app.get("/books_with_class_dep/")
def get_books_with_class_dependency(books: list[Book] = Depends(book_list_dep)) -> list[Book]:
    return books
