from pydantic import BaseModel
from datetime import date
from typing import List
from .userSchema import User
from .productSchema import Product


class OrderItemBase(BaseModel):
    quantity: int
    price_per_unit: int

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    total_price: int
    status: str
    order_date: date
    delivery_address: str
    items: List[OrderItemBase]

    class Config:
        orm_mode = True


class CreateOrder(BaseModel):
    user_id: int


class CreateOrderItem(BaseModel):
    order_id: int
    product_id: int


class Order(OrderBase):
    id: int
    user_id: User


class OrderItem(OrderItemBase):
    id: int
    order_id: Order
    product_id: Product