from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category_id: int


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: int

    class Config:
        from_attributes = True


class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: int
    products: List[ProductRead] = []

    class Config:
        from_attributes = True


class OrderItemBase(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    unit_price: float


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemRead(OrderItemBase):
    id: int

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    user_id: int
    status: str
    order_date: datetime


class OrderCreate(OrderBase):
    pass


class OrderRead(OrderBase):
    id: int
    items: List[OrderItemRead] = []

    class Config:
        from_attributes = True


class ReviewBase(BaseModel):
    product_id: int
    user_id: int
    rating: float
    review_text: str


class ReviewCreate(ReviewBase):
    pass


class ReviewRead(ReviewBase):
    id: int

    class Config:
        from_attributes = True
