from abc import abstractmethod
from typing import List
import models as db
from schemas import *
from sqlalchemy import select
from sqlalchemy.orm import Session


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


class ItemRepository(AbcRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_all(self) -> List[Item]:
        items_db = self._session.execute(select(db.Item)).scalars().all()
        items = [Item.model_validate(item) for item in items_db]
        return items

    def get_by_id(self, id: int) -> Item:
        db_item = self._session.get(db.Item, id)
        return Item.model_validate(db_item)


class SellerRepository(AbcRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_all(self) -> List[Seller]:
        seller_db = self._session.execute(select(db.Seller)).scalars().all()
        sellers = [Seller.model_validate(seller) for seller in seller_db]
        return sellers

    def get_by_id(self, id: int) -> Seller:
        db_seller = self._session.get(db.Seller, id)
        return Seller.model_validate(db_seller)


class CustomerRepository(AbcRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_all(self) -> List[Customer]:
        customer_db = self._session.execute(select(db.Customer)).scalars().all()
        customers = [Customer.model_validate(customer) for customer in customer_db]
        return customers

    def get_by_id(self, id: int) -> Customer:
        db_customer = self._session.get(db.Customer, id)
        return Customer.model_validate(db_customer)


class ShopRepository(AbcRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_all(self) -> List[Shop]:
        shop_db = self._session.execute(select(db.Shop)).scalars().all()
        shops = [Shop.model_validate(shop) for shop in shop_db]
        return shops

    def get_by_id(self, id: int) -> Shop:
        db_shop = self._session.get(db.Shop, id)
        return Shop.model_validate(db_shop)


class OrderRepository(AbcRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_all(self) -> List[Order]:
        order_db = self._session.execute(select(db.Order)).scalars().all()
        orders = [Order.model_validate(order) for order in order_db]
        return orders

    def get_by_id(self, id: int) -> Order:
        db_order = self._session.get(db.Order, id)
        return Order.model_validate(db_order)
