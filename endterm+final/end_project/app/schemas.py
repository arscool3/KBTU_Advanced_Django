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
    user_id: int

class CategoryCreate(BaseModel):
    name: str

class AddressCreate(BaseModel):
    street: str
    city: str
    state: str
    postal_code: str
    country: str
    user_id: int

class PaymentCreate(BaseModel):
    amount: float
    status: str
    transaction_id: str
    user_id: int