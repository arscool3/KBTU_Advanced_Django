from abc import abstractmethod

from sqlalchemy.orm import Session

import database as db

from schemas import Product, Category, User, Order


class AbcRepository:
    @abstractmethod
    def __init__(self, session: Session):
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Product | Category | User | Order:
        raise NotImplementedError()


class UserRepository(AbcRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> User:
        db_user = self._session.get(db.User, id)
        return User.model_validate(db_user)


class CategoryRepository(AbcRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> Category:
        db_category = self._session.get(db.Category, id)
        return Category.model_validate(db_category)


class ProductRepository(AbcRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> Product:
        db_product = self._session.get(db.Product, id)
        return Product.model_validate(db_product)


class OrderRepository(AbcRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> Order:
        db_order = self._session.get(db.Order, id)
        return Order.model_validate(db_order)