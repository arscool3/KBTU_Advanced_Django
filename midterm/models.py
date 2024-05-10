from typing import Annotated

import sqlalchemy as sa

from sqlalchemy.orm import mapped_column, Mapped, relationship

from database import Base

_id = Annotated[int, mapped_column(sa.Integer, primary_key=True)]


class User(Base):
    __tablename__ = 'users'
    id: Mapped[_id]
    username: Mapped[str]
    password: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]

    orders: Mapped[list["Order"]] = relationship(back_populates="client", cascade="all, delete-orphan")


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[_id]
    name: Mapped[Annotated[str, mapped_column(sa.String, unique=True)]]

    products: Mapped['Product'] = relationship(back_populates='category')


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[_id]
    name: Mapped[str]
    price: Mapped[int]
    rating: Mapped[float]
    category_id: Mapped[int] = mapped_column(sa.ForeignKey('categories.id'))

    category: Mapped[Category] = relationship(back_populates='products')
    orders: Mapped['Order'] = relationship(back_populates='product')


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[_id]
    completed: Mapped[bool]
    delivery_address: Mapped[str]

    product_id: Mapped[int] = mapped_column(sa.ForeignKey('products.id'))
    product: Mapped[Product] = relationship(back_populates='orders')

    client_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id"))
    client: Mapped["User"] = relationship(back_populates="orders")
