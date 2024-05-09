from pydantic import BaseModel

# class User(BaseModel):
#     id: int
#     username: str
#     email: str

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float

class OrderCreate(BaseModel):
    name: str
    description: str
    price: float

class CategoryCreate(BaseModel):
    name: str
    description: str
    price: float

class AddressCreate(BaseModel):
    name: str
    description: str
    price: float

class PaymentCreate(BaseModel):
    name: str
    description: str
    price: float