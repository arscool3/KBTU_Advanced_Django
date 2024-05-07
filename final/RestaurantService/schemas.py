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
