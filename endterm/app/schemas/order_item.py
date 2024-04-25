from pydantic import BaseModel

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

class OrderItemCreate(OrderItemBase):
    price: float  # Price at the time of order

class OrderItemOut(OrderItemBase):
    id: int
    order_id: int
    price: float

    class Config:
        orm_mode = True
