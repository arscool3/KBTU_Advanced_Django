import uuid
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from sqlalchemy import Column, Text, ForeignKey
from sqlalchemy_utils import ChoiceType


class Restaurant(Base):
    __tablename__ = 'restaurants'

    RESTAURANT_STATUSES = (
        ('OPEN', 'open'),
        ('CLOSE', 'close')
    )

    id: Mapped[str] = mapped_column(primary_key=True, default=str(uuid.uuid4()))
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    phone_number: Mapped[str] = mapped_column(nullable=False)
    address: Mapped[str]
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    menu: Mapped[List["RestaurantMenuItem"]] = relationship("RestaurantMenuItem", back_populates="restaurant")
    orders: Mapped[List["Order"]] = relationship("Order", back_populates="restaurant")
    status = Column(ChoiceType(RESTAURANT_STATUSES), default="CLOSE")


class RestaurantMenuItem(Base):
    __tablename__ = 'menu_items'

    id: Mapped[str] = mapped_column(primary_key=True, default=str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    image: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = Column(Text)
    restaurant_id: Mapped[str] = mapped_column(ForeignKey("restaurants.id"))
    restaurant: Mapped["Restaurant"] = relationship("Restaurant", back_populates="menu")
    order_item: Mapped["OrderItem"] = relationship("OrderItem", back_populates="restaurant_item")
    order_item_id: Mapped[str] = mapped_column(ForeignKey("order_items.id"))


class Order(Base):
    __tablename__ = 'orders'

    ORDER_STATUSES = (
        ('PENDING', 'pending'),
        ('IN-TRANSIT', 'in-transit'),
        ('DELIVERED', 'delivered'),
    )

    id: Mapped[str] = mapped_column(primary_key=True, default=str(uuid.uuid4()))
    items: Mapped[List["OrderItem"]] = relationship("OrderItem", back_populates="order")
    total: Mapped[int] = mapped_column(nullable=False)
    status = Column(ChoiceType(ORDER_STATUSES), default="PENDING")
    customer_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    customer: Mapped["Customer"] = relationship("Customer", back_populates="orders")
    restaurant_id: Mapped[str] = mapped_column(ForeignKey("restaurants.id"))
    restaurant: Mapped["Restaurant"] = relationship("Restaurant", back_populates="orders")
    courier_id: Mapped[str] = mapped_column(ForeignKey("couriers.id"), nullable=True)
    courier: Mapped["Courier"] = relationship("Courier", back_populates="orders")


class OrderItem(Base):
    __tablename__ = 'order_items'

    id: Mapped[str] = mapped_column(primary_key=True, default=uuid.uuid4())
    price: Mapped[int] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False, default=1)
    order_id: Mapped[str] = mapped_column(ForeignKey("orders.id"))
    order: Mapped["Order"] = relationship("Order", back_populates="items")
    restaurant_item: Mapped["RestaurantMenuItem"] = relationship("RestaurantMenuItem", back_populates="order_item")


class Customer(Base):
    __tablename__ = 'users'

    id: Mapped[str] = mapped_column(primary_key=True, default=str(uuid.uuid4()))
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    phone_number: Mapped[str] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    orders: Mapped[List["Order"]] = relationship("Order", back_populates="customer")


class Courier(Base):
    __tablename__ = 'couriers'

    COURIER_STATUSES = (
        ('OPEN', 'open'),
        ('CLOSE', 'close')
    )

    id: Mapped[str] = mapped_column(primary_key=True, default=str(uuid.uuid4()))
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    phone_number: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    orders: Mapped[List["Order"]] = relationship("Order", back_populates="courier")
    status = Column(ChoiceType(COURIER_STATUSES), default="CLOSE")
