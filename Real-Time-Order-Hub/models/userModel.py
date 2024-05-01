from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, Date, BigInteger
from sqlalchemy.orm import relationship
from database.db import Base
from sqlalchemy.dialects.postgresql import ENUM

status_enum = ENUM('new', 'processing', 'shipped', 'delivered', name='status_enum', create_type=False)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    address = Column(String, nullable=False)

    chat_ids = relationship("UserChatID", back_populates="user")


class UserChatID(Base):
    __tablename__ = 'user_chat_ids'
    id = Column(Integer, primary_key=True)
    chat_id = Column(BigInteger, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship("User", back_populates="chat_ids")


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    total_price = Column(Integer, nullable=False)
    status = Column(status_enum, nullable=False)
    order_date = Column(DateTime, nullable=False)
    delivery_address = Column(String, nullable=False)
    expected_delivery_date = Column(Date, nullable=True)

    items = relationship("Order_Item", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = 'order_items'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id', ondelete='CASCADE'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_per_unit = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")
