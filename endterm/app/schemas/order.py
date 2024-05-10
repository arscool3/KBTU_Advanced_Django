from pydantic import BaseModel
from datetime import datetime
from typing import List
from .order_item import OrderItemOut
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "PENDING"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"

class OrderBase(BaseModel):
    status: OrderStatus = OrderStatus.PENDING

class OrderCreate(OrderBase):
    pass

class OrderOut(OrderBase):
    id: int
    user_id: int
    created_at: datetime
    items: List[OrderItemOut] = []

    class Config:
        orm_mode = True
