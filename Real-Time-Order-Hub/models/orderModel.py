from sqlalchemy import (
    Integer, String, ForeignKey, DateTime, Date
)
import sqlalchemy
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing_extensions import Annotated
from database import Base


_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]


class Order(Base):
    __tablename__ = 'orders'
    id: Mapped[_id]
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    total_price: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    order_date: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    delivery_address: Mapped[str] = mapped_column(String, nullable=False)
    expected_delivery_date: Mapped[Date] = mapped_column(Date, nullable=True)

    items: Mapped[list] = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = 'order_items'
    id: Mapped[_id]
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey('orders.id', ondelete='CASCADE'), nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('products.id'), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price_per_unit: Mapped[int] = mapped_column(Integer, nullable=False)

    order: Mapped['Order'] = relationship("Order", back_populates="items")
    product: Mapped['Product'] = relationship("Product")