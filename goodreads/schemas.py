from typing import Optional, List
from pydantic import BaseModel

class Goodreads(BaseModel):
    id: Optional[int]
    name: Optional[str]
    description: Optional[str]

class User(BaseModel, Goodreads):
    reviews: Optional[List['BookReview']]

class Genre(BaseModel, Goodreads):
    book: Optional['Book']

class Book(BaseModel, Goodreads):
    author_id: Optional[int]
    author: Optional['Author']
    genre_id: Optional[int]
    genres: Optional[List[Genre]]
    reviews: Optional[List['BookReview']]

class Quote(BaseModel):
    id: Optional[int]
    description: Optional[str]
    author_id: Optional[int]
    author: Optional['Author']

class Author(BaseModel, Goodreads):
    books: Optional[List[Book]]
    quotes: Optional[List[Quote]]

class BookReview(BaseModel):
    id: Optional[int]
    review: Optional[str]
    rating: Optional[int]
    user_id: Optional[int]
    user: Optional[User]
    book_id: O
