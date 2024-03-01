from datetime import date
from typing import Annotated

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, mapped_column, Mapped, relationship

url = 'postgresql://postgres:postgres@localhost:5434/postgres'
engine = create_engine(url)
session = Session(engine)

Base = declarative_base()

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]


# User -> Order: One to Many
# Category -> Product: One to Many
# Product -> Category: Many to One

class User(Base):
    __tablename__ = 'users'

    id: Mapped[_id]
    name: Mapped[str]
    created_at: Mapped[date] = mapped_column(sqlalchemy.DATE, default=date.today())

    orders: Mapped['Order'] = relationship('Order', back_populates='user')


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[_id]
    name: Mapped[str]
    created_at: Mapped[date] = mapped_column(sqlalchemy.DATE, default=date.today())
    products: Mapped['Product'] = relationship(back_populates='category')


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[_id]
    name: Mapped[str]
    category_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('categories.id'))
    category: Mapped[Category] = relationship(back_populates='products')


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[_id]
    name: Mapped[str]

    user_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('users.id'))
    user: Mapped[User] = relationship('User', back_populates='orders')