from typing import Union, ForwardRef, List
from datetime import datetime
from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str

    class Config:
        from_attributes = True


class User(UserCreate):
    id: int


class GenreCreate(BaseModel):
    name: str

    class Config:
        from_attributes = True


class Genre(GenreCreate):
    id: int


class PublisherCreate(BaseModel):
    name: str
    address: str

    class Config:
        from_attributes = True


class Publisher(PublisherCreate):
    id: int


class BookCreate(BaseModel):
    title: str
    desc: str
    author: str
    price: int
    genre_id: int
    publisher_id: int

    class Config:
        from_attributes = True


class Book(BookCreate):
    id: int
    genres: Genre
    publishers: Publisher


class TokenData(BaseModel):
    username: str = None


class OrderCreate(BaseModel):
    user_id: int
    total_price: float
    status: str


class OrderItemCreate(BaseModel):
    order_id: int
    book_id: int
    quantity: int
    price: float


class OrderItem(OrderItemCreate):
    id: int
    book: Book


class Order(OrderCreate):
    id: int
    date: datetime
    user: User
    items: List[ForwardRef('OrderItem')] = []


Order.update_forward_refs()


ReturnType = Union[Book, Genre, Publisher, Order, OrderItem]