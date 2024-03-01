from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import punq

app = FastAPI()

books = []
authors = []
publishers = []

class Author(BaseModel):
    name: str
    books: List[int] = []


class Publisher(BaseModel):
    name: str
    books: List[int] = []


class Book(BaseModel):
    id: int
    title: str
    author_id: int
    publisher_id: int


class BookRepository:
    def __init__(self):
        self.counter = 0
    
    def add_book(self, book: Book):
        self.counter += 1
        book.id = self.counter
        books.append(book)
        return book


    def get_book_by_id(self, book_id: int):
        for book in books:
            if book.id == book_id:  
                return book
        return None


    def delete_book(self, book_id: int):
        for i, book in enumerate(books):
            if book.id == book_id: 
                del books[i]
                return book
        return None


class AuthorRepository:
    def add_author(self, author: Author):
        authors.append(author)
        return author


class PublisherRepository:
    def add_publisher(self, publisher: Publisher):
        publishers.append(publisher)
        return publisher


def get_container() -> punq.Container:
    container = punq.Container()
    container.register(BookRepository)
    container.register(AuthorRepository)
    container.register(PublisherRepository)
    return container


@app.post("/books/", response_model=Book)
def create_book(book_repo: BookRepository = Depends(get_container().resolve(BookRepository).add_book)):
    return book_repo


@app.get("/books/{book_id}", response_model=Book)
def read_book(book_id: int, book_repo: BookRepository = Depends(get_container().resolve(BookRepository).get_book_by_id)):
    book = book_repo.get_book_by_id(book_id)
    return book


@app.delete("/books/{book_id}", response_model=Book)
def delete_book(book_id: int, book_repo: BookRepository = Depends(get_container().resolve)):
    deleted_book = book_repo.delete_book(book_id)
    return deleted_book


@app.post("/authors/", response_model=Author)
def create_author(author: Author, author_repo: AuthorRepository = Depends(get_container().resolve)):
    return author_repo.add_author(author)


@app.post("/publishers/", response_model=Publisher)
def create_publisher(publisher: Publisher, publisher_repo: PublisherRepository = Depends(get_container().resolve)):
    return publisher_repo.add_publisher(publisher)
