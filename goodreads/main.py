from fastapi import FastAPI, Depends
from sqlalchemy.orm.session import Session
from sqlalchemy import select

from database import session
from schemas import CreateUser, User,Author,CreateAuthor,Book,CreateBook
import models as db

app = FastAPI()



def get_db():
    try:
        yield session
        session.commit()
    except:
        raise
    finally:
        session.close()

@app.post("/users")
def add_users(user: CreateUser) -> str:
    session.add(db.User(**user.model_dump()))
    session.commit()
    session.close()
    return "User was added"

@app.get("/users")
def get_users():
    db_users = session.execute(select(db.User)).scalars().all()
    users = []
    for db_user in db_users:
        users.append(User.model_validate(db_user))
    return users

@app.post("/authors")
def add_authors(author: CreateAuthor) -> str:
    session.add(db.Author(**author.model_dump()))
    session.commit()
    session.close()
    return "Author"

@app.get("/authors")
def get_authors():
    db_authors = session.execute(select(db.Author)).scalars().all()
    authors = []
    for db_author in db_authors:
        authors.append(Author.model_validate(db_author))
    return authors


@app.post("/books")
def add_books(book: CreateBook) -> str:
    session.add(db.Book(**book.model_dump()))
    session.commit()
    session.close()
    return "Book"

@app.get("/books")
def get_books():
    db_books = session.execute(select(db.Book)).scalars().all()
    books = []
    for db_book in db_books:
        books.append(Book.model_validate(db_book))
    return books
