from pydantic import BaseModel
from typing import Union

class OrderBase(BaseModel):
    name: str
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
    shop: Shop
    order: Order


class Shop(ShopBase):
    id: int
    item: Item
    seller: Seller


class Seller(SellerBase):
    id: int
    shop: Shop


class Order(OrderBase):
    id: int
    item: Item
    customer: 'Customer'


class Customer(CustomerBase):
    id: int
    order: Order


ReturnType = Union[Order, Seller, Customer, Shop, Item]

