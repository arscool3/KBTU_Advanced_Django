from typing import Annotated
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import relationship, mapped_column, Mapped
from database import Base
from datetime import datetime


_id = Annotated[int, mapped_column(Integer, primary_key=True, autoincrement=True)]


'''
RELATIONSHIPS - 6
user 1<->* order
user 1<->* review 
product *<->1 category
product 1<->* review
orderItem *<->1 product
orderItem *<->1 order
'''


class User(Base):
    __tablename__ = "users"

    id: Mapped[_id]
    username: Mapped[str]
    password: Mapped[str]
    email: Mapped[str]

    orders: Mapped[list["Order"]] = relationship("Order", back_populates="user")
    reviews: Mapped["Review"] = relationship("Review", back_populates="user")


class Product(Base):
    __tablename__ = "products"

    id: Mapped[_id]
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[float]
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))

    category: Mapped["Category"] = relationship("Category", back_populates="products")
    reviews: Mapped["Review"] = relationship("Review", back_populates="product")


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[_id]
    name: Mapped[str]
    description: Mapped[str]

    products: Mapped[list["Product"]] = relationship("Product", back_populates="category")


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[_id]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    status: Mapped[str]
    order_date: Mapped[datetime]

    user: Mapped["User"] = relationship("User", back_populates="orders")
    items: Mapped[list["OrderItem"]] = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[_id]
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    quantity: Mapped[int]
    unit_price: Mapped[float]

    order: Mapped["Order"] = relationship("Order", back_populates="items")
    product: Mapped["Product"] = relationship("Product")


class Review(Base):
    __tablename__ = 'reviews'

    id: Mapped[_id]
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    rating: Mapped[int]
    review_text: Mapped[str]

    product: Mapped["Product"] = relationship("Product", back_populates="reviews")
    user: Mapped["User"] = relationship("User", back_populates="reviews")
