from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm.session import Session
from sqlalchemy import select

from database import session,engine
from typing import List
from schemas import CreateUser, User,Author,CreateAuthor,Book,CreateBook,BookReview,CreateBookReview,Quote,CreateQuote,Genre,CreateGenre
import models as db
db.Base.metadata.create_all(bind=engine)

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
def add_users(user: CreateUser,session: Session = Depends(get_db)) -> str:
    session.add(db.User(**user.model_dump()))
    session.commit()
    session.close()
    return "User was added"

@app.get("/users")
def get_users(session: Session = Depends(get_db)):
    db_users = session.execute(select(db.User)).scalars().all()
    users = []
    for db_user in db_users:
        users.append(User.model_validate(db_user))
    return users

@app.post("/authors")
def add_authors(author: CreateAuthor,session: Session = Depends(get_db)) -> str:
    session.add(db.Author(**author.model_dump()))
    session.commit()
    session.close()
    return "Author"

@app.get("/authors")
def get_authors(session: Session = Depends(get_db)):
    db_authors = session.execute(select(db.Author)).scalars().all()
    authors = []
    for db_author in db_authors:
        authors.append(Author.model_validate(db_author))
    return authors


@app.post("/books")
def add_books(book: CreateBook,session: Session = Depends(get_db)) -> str:
    session.add(db.Book(**book.model_dump()))
    session.commit()
    session.close()
    return "Book"

@app.get("/books")
def get_books(session: Session = Depends(get_db)):
    db_books = session.execute(select(db.Book)).scalars().all()
    books = []
    for db_book in db_books:
        books.append(Book.model_validate(db_book))
    return books


@app.post("/quotes")
def add_quotes(quote: CreateQuote,session: Session = Depends(get_db)) -> str:
    session.add(db.Quote(**quote.model_dump()))
    session.commit()
    session.close()
    return "Quote"

@app.get("/quotes")
def get_quotes(session: Session = Depends(get_db)):
    db_quotes = session.execute(select(db.Quote)).scalars().all()
    quotes= []
    for db_quote in db_quotes:
        quotes.append(Quote.model_validate(db_quote))
    return quotes


@app.post("/bookreviews")
def add_bookreviews(bookreview:CreateBookReview,session: Session = Depends(get_db)) -> str:
    session.add(db.BookReview(**bookreview.model_dump()))
    session.commit()
    session.close()
    return "BookReview"

@app.get("/bookreviews")
def get_bookreviews(session: Session = Depends(get_db)):
    db_bookreviews= session.execute(select(db.BookReview)).scalars().all()
    bookreviews = []
    for db_bookreview in db_bookreviews:
        bookreviews.append(BookReview.model_validate(db_bookreview))
    return bookreviews

@app.post("/genres")
def add_genres(genre:CreateGenre,session: Session = Depends(get_db)) -> str:
    session.add(db.Genre(**genre.model_dump()))
    session.commit()
    session.close()
    return "Genre"

@app.get("/genres")
def get_genres(session: Session = Depends(get_db)):
    db_genres= session.execute(select(db.Genre)).scalars().all()
    genres = []
    for db_genre in db_genres:
        genres.append(Genre.model_validate(db_genre))
    return genres

@app.get("/books/{author_id}", response_model=List[Book])
def get_books_by_author(author_id: int, session: Session = Depends(get_db)):
    author = session.query(Author).filter(Author.id == author_id).first()
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author.books

@app.get("/bookreviews/{user_id}", response_model=List[BookReview])
def get_bookreviews_by_user(user_id: int, session: Session = Depends(get_db)):
    user = session.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user.bookreviews

@app.get("/quotes/{author_id}", response_model=List[Quote])
def get_quotes_by_author(author_id: int, session: Session = Depends(get_db)):
    author = session.query(Author).filter(Author.id == author_id).first()
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author.quotes
