from abc import abstractmethod
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


class GenreRepository(AbcRepository):

    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> Genre:
        db_genre = self._session.get(db.Genre, id)
        return Genre.model_validate(db_genre)


class PublisherRepository(AbcRepository):

    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> Publisher:
        db_publisher = self._session.get(db.Publisher, id)
        return Publisher.model_validate(db_publisher)


class OrderRepository(AbcRepository):

    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> Order:
        db_order = self._session.get(db.Order, id)
        return Order.model_validate(db_order)


class OrderItemRepository(AbcRepository):

    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> OrderItem:
        db_order_item = self._session.get(db.OrderItem, id)
        return OrderItem.model_validate(db_order_item)

