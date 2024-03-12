from abc import abstractmethod

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

import models as db
from schemas import Book, Genre, Publisher, Order, OrderItem, ReturnType


class AbcRepository:

    @abstractmethod
    def __init__(self, session: Session):
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> ReturnType:
        raise NotImplementedError()


class BookRepository(AbcRepository):

    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> Book:
        db_book = self._session.get(db.Book, id)
        return Book.model_validate(db_book)

    def get_all(self) -> list[Book]:
        db_books = self._session.execute(select(db.Book)).scalars().all()
        books = []
        for db_book in db_books:
            books.append(Book.model_validate(db_book))
        return books


class GenreRepository(AbcRepository):

    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> Genre:
        db_genre = self._session.get(db.Genre, id)
        return Genre.model_validate(db_genre)

    def get_all(self) -> list[Genre]:
        db_genres = self._session.execute(select(db.Genre)).scalars().all()
        genres = []
        for db_genre in db_genres:
            genres.append(Genre.model_validate(db_genre))
        return genres



class PublisherRepository(AbcRepository):

    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> Publisher:
        db_publisher = self._session.get(db.Publisher, id)
        return Publisher.model_validate(db_publisher)

    def get_all(self) -> list[Publisher]:
        db_publishers = self._session.execute(select(db.Publisher)).scalars().all()
        publishers = []
        for db_publisher in db_publishers:
            publishers.append(Publisher.model_validate(db_publisher))
        return publishers


class OrderRepository(AbcRepository):

    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> Order:
        db_order = self._session.get(db.Order, id)
        return Order.model_validate(db_order)

    def get_all(self) -> list[Order]:
        db_orders = self._session.execute(select(db.Order)).scalars().all()
        orders = []
        for db_order in db_orders:
            orders.append(Order.model_validate(db_order))
        return orders


class OrderItemRepository(AbcRepository):

    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> OrderItem:
        db_order_item = self._session.get(db.OrderItem, id)
        return OrderItem.model_validate(db_order_item)

    def get_all(self) -> list[OrderItem]:
        db_order_items = self._session.execute(select(db.OrderItem)).scalars().all()
        order_items = []
        for db_order_item in db_order_items:
            order_items.append(OrderItem.model_validate(db_order_item))
        return order_items
