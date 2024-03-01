import punq
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import schemas
from database import engine
from repository import AbcRepository, UserRepository, AuthorRepository, BookCategoryRepository, BookRepository
from schemas import CreateUser, CreateBook, CreateAuthor, CreateBookCategory
import models

app = FastAPI()

session = Session(engine)


def create_user_dep(user: CreateUser):
    session.add(models.User(**user.model_dump()))
    session.commit()
    return """User created"""


class CreateAuthorDep:
    def __call__(self, author: CreateAuthor):
        session.add(models.BookAuthor(**author.model_dump()))
        session.commit()
        return author


def create_book_category_dep(category: CreateBookCategory):
    session.add(models.BookCategory(**category.model_dump()))
    session.commit()
    return category


def create_book_dep(book: CreateBook):
    session.add(models.Book(**book.model_dump()))
    session.commit()
    return """Book created"""


class GetAllDependency:
    def __init__(self, repo: AbcRepository):
        self.repo = repo

    def __call__(self):
        return self.repo.get_all()


def get_container(repository: type[AbcRepository]) -> punq.Container:
    container = punq.Container()
    container.register(AbcRepository, repository, instance=repository(session=session))
    container.register(GetAllDependency)
    return container


@app.post("/users")
async def create_user(dep_fun: CreateUser = Depends(create_user_dep)):
    return dep_fun


@app.post("/authors")
async def create_author(dep: CreateAuthor = Depends(CreateAuthorDep())):
    return dep


@app.post("/categories")
async def create_category(dep_fun: CreateBookCategory = Depends(create_book_category_dep)):
    return dep_fun


@app.post("/books")
async def create_book(dep_fun: CreateBook = Depends(create_book_dep)):
    return dep_fun


@app.get("/users")
async def get_users(dep: list[schemas.User] = Depends(get_container(UserRepository).resolve(GetAllDependency))):
    return dep


@app.get("/authors")
async def get_authors(dep: list[schemas.Author] = Depends(get_container(AuthorRepository).resolve(GetAllDependency))):
    return dep


@app.get("/book_categories")
async def get_book_categories(dep: list[schemas.BookCategory] = Depends(get_container(BookCategoryRepository).resolve(GetAllDependency))):
    return dep


@app.get("/books")
async def get_books(dep: list[schemas.Book] = Depends(get_container(BookRepository).resolve(GetAllDependency))):
    return dep
