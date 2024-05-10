from typing import List, Any
from pydantic import BaseModel


class OrderItem(BaseModel):
    id: str
    price: int
    quantity: int
    order_id: str
    restaurant_item_id: str

    class Config:
        from_attributes = True


class CreateOrderItem(BaseModel):
    quantity: int
    restaurant_item_id: str


class Order(BaseModel):
    id: str
    customer_id: str
    status: str
    restaurant_id: str
    courier_id: str
    total: int

    class Config:
        from_attributes = True


class CreateOrder(BaseModel):
    customer_id: str
    restaurant_id: str


class Restaurant(BaseModel):
    id: str
    address: str
    email: str
    status: str

    class Config:
        from_attributes = True
