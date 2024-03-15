from pydantic import BaseModel


class BaseCategory(BaseModel):
    name: str

    class Config:
        from_attributes = True


class BaseProduct(BaseModel):
    name: str
    price: int
    rating: int

    class Config:
        from_attributes = True


class BaseOrder(BaseModel):
    completed: bool
    delivery_address: str

    class Config:
        from_attributes = True


class CreateProduct(BaseProduct):
    category_id: int


class CreateOrder(BaseOrder):
    product_id: int
