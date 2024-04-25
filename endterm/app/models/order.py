from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum, sql
from sqlalchemy.orm import relationship
from . import Base
import enum

class OrderStatus(enum.Enum):
    PENDING = "PENDING"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    created_at = Column(DateTime, server_default=sql.func.now())

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")