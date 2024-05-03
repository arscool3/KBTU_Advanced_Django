from typing import List
from pydantic import BaseModel


class OrderItem(BaseModel):
    id: str
    price: int
    quantity: int
    order_id: str
    restaurant_item: str


class Order(BaseModel):
    id: str
    customer_id: str
    items: List[OrderItem]
    status: str
    restaurant_id: str
    courier_id: str
    total: int


class CreateOrder(BaseModel):
    customer_id: str
    restaurant_id: str
    courier: str

