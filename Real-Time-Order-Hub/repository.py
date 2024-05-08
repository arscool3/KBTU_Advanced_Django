from abc import abstractmethod
from typing import List
import models.productModel as db
from schemas import *
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Union


ReturnType = Union[User, Product, UserChatID, Order, OrderItem]


class AbcRepository:
    @abstractmethod
    def __init__(self, session: Session):
        pass

    @abstractmethod
    def get_all(self) -> List[ReturnType]:
        raise NotImplementedError()

    @abstractmethod
    def get_by_id(self, id: int) -> ReturnType:
        raise NotImplementedError()


class ProductRepository(AbcRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_all(self) -> List[Product]:
        products_db = self._session.execute(select(db.Product)).scalars().all()
        products = [Product.model_validate(product) for product in products_db]
        return products

    def get_by_id(self, id: int) -> Product:
        db_product = self._session.get(db.Product, id)
        return Product.model_validate(db_product)

