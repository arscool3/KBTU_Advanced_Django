from abc import abstractmethod
from sqlalchemy.orm import Session

import models as db
from schemas import Item, User, Category, ReturnType


class AbcRepository:

    @abstractmethod
    def __init__(self, session: Session):
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> ReturnType:
        raise NotImplementedError()


class ItemRepository(AbcRepository):

    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> Item:
        db_item = self._session.get(db.Item, id)
        return Item.model_validate(db_item)


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
