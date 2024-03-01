from datetime import date
from pydantic import BaseModel

class BaseAuthor(BaseModel):
    name: str
    birth_date: date

    class Config:
        from_attributes = True

class Author(BaseAuthor):
    id: int

    def dict(self, **kwargs):
        return super().dict(exclude={'books'}, **kwargs)

class CreateAuthor(BaseAuthor):
    pass

class BaseBook(BaseModel):
    title: str
    publication_date: date

    class Config:
        from_attributes = True

class Book(BaseBook):
    id: int
    author: Author
    genre: 'Genre'
    publisher: 'Publisher'

    def dict(self, **kwargs):
        return super().dict(exclude={'author': {'books'}, 'genre': {'books'}, 'publisher': {'books'}}, **kwargs)

class CreateBook(BaseBook):
    author_id: int
    genre_id: int
    publisher_id: int

class BaseGenre(BaseModel):
    name: str

    class Config:
        from_attributes = True

class Genre(BaseGenre):
    id: int

    def dict(self, **kwargs):
        return super().dict(exclude={'books'}, **kwargs)

class CreateGenre(BaseGenre):
    pass

class BasePublisher(BaseModel):
    name: str

    class Config:
        from_attributes = True

class Publisher(BasePublisher):
    id: int

    def dict(self, **kwargs):
        return super().dict(exclude={'books'}, **kwargs)

class CreatePublisher(BasePublisher):
    pass
