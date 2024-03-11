from typing import Annotated

import sqlalchemy
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import func
from datetime import datetime

from database import Base

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]


class User(Base):
    __tablename__ = 'users'
    id: Mapped[_id]
    username: Mapped[str]
    password: Mapped[str]


class Genre(Base):
    __tablename__ = 'genres'
    id: Mapped[_id]
    name: Mapped[str]
    book: Mapped['Book'] = relationship(back_populates='genres')


class Publisher(Base):
    __tablename__ = 'publishers'
    id: Mapped[_id]
    name: Mapped[str]
    address: Mapped[str]
    book: Mapped['Book'] = relationship(back_populates='publishers')


class Book(Base):
    __tablename__ = 'books'
    id: Mapped[_id]
    title: Mapped[str]
    desc: Mapped[str]
    author: Mapped[str]
    price: Mapped[int]
    genre_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('genres.id'))
    publisher_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('publishers.id'))
    genres: Mapped[list[Genre]] = relationship(back_populates='book')
    publishers: Mapped[list[Publisher]] = relationship(back_populates='book')


class Order(Base):
    __tablename__ = 'orders'
    id: Mapped[_id]
    user_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('users.id'))
    date: Mapped[datetime] = mapped_column(default=func.now())
    total_price: Mapped[float]
    status: Mapped[str]
    user: Mapped[User] = relationship(back_populates='orders')
    items: Mapped[list['OrderItem']] = relationship(back_populates='order')


class OrderItem(Base):
    __tablename__ = 'order_items'
    id: Mapped[_id]
    order_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('orders.id'))
    book_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('books.id'))
    quantity: Mapped[int]
    price: Mapped[float]
    order: Mapped[Order] = relationship(back_populates='items')
    book: Mapped[Book] = relationship(back_populates='order_items')


User.orders = relationship('Order', back_populates='user')
Book.order_items = relationship('OrderItem', back_populates='book')
