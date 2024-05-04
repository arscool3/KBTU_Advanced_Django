#sqlaclhemy models
# 6 Models, 4 relationships(user, book, bookreview, Author, Quote,bookshelf)
from typing import Annotated
import sqlalchemy
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database import Base

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]

# genres and books relationship, author and books relationship, user and reviews relationship
#reviews and books relationship, quote and author
class Goodreads:
    id: Mapped[_id]
    name: Mapped[str]
    description: Mapped[str]

class User(Base, Goodreads):
    __tablename__ = 'users'
    bookreviews: Mapped['BookReview'] = relationship("BookReview", back_populates='user')

class Genre(Base,Goodreads):
    __tablename__ = 'genres'
    books: Mapped['Book'] = relationship("Book", back_populates='genre')

class Book(Base,Goodreads):
    __tablename__ = 'books'
    author_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('authors.id'))
    author: Mapped['Author'] = relationship("Author", back_populates='books')
    genre_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('genres.id'))
    genre: Mapped['Genre'] = relationship("Genre",back_populates='books')
    reviews: Mapped['BookReview'] = relationship("BookReview", back_populates='book')

class Quote(Base):
    __tablename__='quotes'
    id: Mapped[_id]
    description: Mapped[str]    
    author_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('authors.id'))
    author: Mapped['Author'] = relationship("Author", back_populates='quotes')   
    
class Author(Base,Goodreads):
    __tablename__ = 'authors'
    books: Mapped[Book] = relationship("Book", back_populates='author')
    quotes:Mapped[Quote]=relationship("Quote",back_populates='author')

class BookReview(Base):
    __tablename__='bookreviews'
    id: Mapped[_id]
    review: Mapped[str] 
    rating:Mapped[int]
    user_id:Mapped[int]=mapped_column(sqlalchemy.ForeignKey('users.id'))
    user:Mapped[User]=relationship("User",back_populates='bookreviews')
    book_id: Mapped[int]=mapped_column(sqlalchemy.ForeignKey('books.id'))
    book: Mapped[Book] = relationship("Book", back_populates='reviews')

