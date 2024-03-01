from fastapi.params import Depends
from pydantic import BaseModel
from sqlalchemy import select, insert
from fastapi import FastAPI

import models as db
import punq
from database import session
from schemas import Author, CreateAuthor, Book, CreateBook, Genre, CreateGenre, CreatePublisher , Publisher
from repository import AuthorRepository, BookRepository, GenreRepository, PublisherRepository, AbcRepository

app = FastAPI()

class Dependency:
    def __init__(self, repo: AbcRepository):
        self.repo = repo

    def __call__(self, id: int) -> Author | Book | Publisher | Genre:
        return self.repo.get_by_id(id)

def get_container(repository: type[AbcRepository]) -> punq.Container:
    container = punq.Container()
    container.register(AbcRepository, repository, instance=repository(session=session))
    container.register(Dependency)
    return container

@app.post("/authors")
def add_author(author: CreateAuthor) -> str:
    session.add(db.Author(**author.dict()))
    session.commit()
    session.close()
    return "Author added"

@app.post("/books")
def add_book(book: CreateBook) -> str:
    session.add(db.Book(**book.dict()))
    session.commit()
    session.close()
    return "Book added"

@app.post("/genres")
def add_genre(genre: CreateGenre) -> str:
    session.add(db.Genre(**genre.dict()))
    session.commit()
    session.close()
    return "Genre added"

@app.get("/authors/{author_id}")
def get_author(author_id: int, dependency_func: BaseModel = Depends(get_container(AuthorRepository).resolve(Dependency))):
    return dependency_func

@app.get("/books/{book_id}")
def get_book(book_id: int, dependency_func: BaseModel = Depends(get_container(BookRepository).resolve(Dependency))):
    return dependency_func

@app.get("/genres/{genre_id}")
def get_genre(genre_id: int, dependency_func: BaseModel = Depends(get_container(GenreRepository).resolve(Dependency))):
    return dependency_func

@app.post("/publishers")
def add_publisher(publisher: CreatePublisher) -> str:
    session.add(db.Publisher(**publisher.dict()))
    session.commit()
    session.close()
    return "Publisher added"

@app.get("/publishers/{publisher_id}")
def get_publisher(publisher_id: int, dependency_func: BaseModel = Depends(get_container(PublisherRepository).resolve(Dependency))):
    return dependency_func
