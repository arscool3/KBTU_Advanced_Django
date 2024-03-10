from typing_extensions import Annotated, List
import sqlalchemy
from sqlalchemy.orm import mapped_column, relationship, Mapped
from database import Base

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]


class User:
    id: Mapped[_id]
    name: Mapped[str]


class Order(Base):
    __tablename__ = "orders"
    id: Mapped[_id]
    quantity: Mapped[int]
    total_value: Mapped[int]
    item_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('items.id'))
    customer_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('customers.id'))
    item: Mapped['Item'] = relationship(back_populates='order')
    customer: Mapped['Customer'] = relationship(back_populates='order')


class Item(Base):
    __tablename__ = "items"
    id: Mapped[_id]
    name: Mapped[str]
    price: Mapped[int]
    description: Mapped[str]
    rating: Mapped[float]
    shop: Mapped['Shop'] = relationship(back_populates='items')
    order: Mapped[List[Order]] = relationship(back_populates='item')


class Customer(User, Base):
    __tablename__ = "customers"
    id: Mapped[_id]
    name: Mapped[str]
    order: Mapped[List[Order]] = relationship(back_populates='customer')


class Seller(User, Base):
    __tablename__ = "sellers"
    id: Mapped[_id]
    name: Mapped[str]
    shop: Mapped['Shop'] = relationship(back_populates='seller')


class Shop(User, Base):
    __tablename__ = "shops"
    seller_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('sellers.id'))
    item_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('items.id'))
    seller: Mapped['Seller'] = relationship(back_populates='shop')
    items: Mapped[List[Item]] = relationship(back_populates='shop')



