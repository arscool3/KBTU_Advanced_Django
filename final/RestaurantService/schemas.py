from pydantic import BaseModel


class CreateMenuItem(BaseModel):
    name: str
    price: int
    image: str
    description: str
    restaurant_id: str


class UpdateMenuItem(BaseModel):
    name: str
    price: str
    image: str
    description: str


class Order(BaseModel):
    id: str
    total: int
    status: str
    customer_id: str
    courier_id: str
    restaurant_id: str

    class Config:
        from_attributes = True

