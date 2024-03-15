from pydantic import BaseModel


class User(BaseModel):
    class Config:
        from_attributes = True

    id: str
    username: str
    first_name: str
    last_name: str


class CreateUser(BaseModel):
    username: str
    first_name: str
    last_name: str
    password: str


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
