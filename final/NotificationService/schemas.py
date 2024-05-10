from pydantic import BaseModel


class Order(BaseModel):
    id: str
    total: int
    status: str
    customer_id: str
    courier_id: str
    restaurant_id: str

    class Config:
        from_attributes = True
