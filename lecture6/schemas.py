from datetime import date
from pydantic import BaseModel


class BaseUser(BaseModel):
    name: str

    class Config:
        from_attributes = True

class User(BaseUser):
    id: int

class CreateUser(BaseUser):
    pass


class BaseCategory(BaseModel):
    name: str
    created_at: date

    class Config:
        from_attributes = True

class CreateCategory(BaseCategory):
    pass

class Category(BaseCategory):
    id: int


class BaseProduct(BaseModel):
    name: str
    category: Category

    class Config:
        from_attributes = True


class CreateProduct(BaseProduct):
    category_id: int


class ProductCategory(BaseProduct):
    name: str

class Product(BaseProduct):
    id: int
    category = ProductCategory


class BaseOrder(BaseModel):
    name: str

    class Config:
        from_attributes = True

class Order(BaseOrder):
    id: int

class CreateOrder(BaseOrder):
    pass