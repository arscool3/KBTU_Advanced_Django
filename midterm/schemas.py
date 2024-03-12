from pydantic import BaseModel
from typing import Union


class OrderBase(BaseModel):
    quantity: int
    total_value: int

    class Config:
        from_attributes = True


class ItemBase(BaseModel):
    name: str
    price: int
    description: str
    rating: float

    class Config:
        from_attributes = True


class SellerBase(BaseModel):
    name: str

    class Config:
        from_attributes = True


class CustomerBase(BaseModel):
    name: str

    class Config:
        from_attributes = True


class ShopBase(BaseModel):
    name: str

    class Config:
        from_attributes = True


class CreateOrder(OrderBase):
    item_id: int
    customer_id: int


class CreateShop(ShopBase):
    item_id: int
    seller_id: int


class CreateSeller(SellerBase):
    pass


class CreateItem(ItemBase):
    pass


class CreateCustomer(CustomerBase):
    pass


class Item(ItemBase):
    id: int


class Seller(SellerBase):
    id: int


class Shop(ShopBase):
    id: int
    item: Item
    seller: Seller


class Customer(CustomerBase):
    id: int


class Order(OrderBase):
    id: int
    item: Item
    customer: Customer


ReturnType = Union[Order, Seller, Customer, Shop, Item]

