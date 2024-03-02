from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Mapped

class CoffeeBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: Optional[int] = None

class CoffeeCreate(CoffeeBase):
    pass

class Coffee(CoffeeBase):
    id: int

    class Config:
        orm_mode = True

class CoffeeShopBase(BaseModel):
    name: str
    rating: int

class CoffeeShopCreate(CoffeeShopBase):
    pass

class CoffeeShop(CoffeeShopBase):
    id: int
    owner_id: int
    coffees: List[Coffee] = []

    class Config:
        orm_mode = True

class CoffeeShopOwnerBase(BaseModel):
    name: str

class CoffeeShopOwnerCreate(CoffeeShopOwnerBase):
    pass

class CoffeeShopOwner(CoffeeShopOwnerBase):
    id: int
    coffee_shops: List[CoffeeShop] = []

    class Config:
        orm_mode = True
