from pydantic import BaseModel
from typing import Union


class ItemBase(BaseModel):
    name: str
    description: str
    user_id: int

    class Config:
        from_attributes = True


class CreateItem(ItemBase):
    pass


class Item(ItemBase):
    id: int


class UserBase(BaseModel):
    name: str
    email: str

    class Config:
        from_attributes = True


class CreateUser(UserBase):
    pass


class User(UserBase):
    id: int
    items: list[Item] = []


class CategoryBase(BaseModel):
    name: str

    class Config:
        from_attributes = True


class CreateCategory(CategoryBase):
    pass


class Category(CategoryBase):
    id: int
    items: list[Item] = []


ReturnType = Union[Item, User, Category]