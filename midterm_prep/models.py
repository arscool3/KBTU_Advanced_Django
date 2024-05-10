from typing import Annotated
from datetime import date

import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.database import Base

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]

class CoffeeShop(Base):
    __tablename__ = 'coffe_shops'

    id: Mapped[_id]
    name: Mapped[str]
    rating: Mapped[int]
    owner: Mapped['CoffeeShopOwner'] = relationship(back_populates='coffee_shop')
    coffees: Mapped['Coffee'] = relationship(back_populates='coffee_shop')

class CoffeeShopOwner(Base):
    __tablename__ = 'coffee_shop_owners'

    id: Mapped[_id]
    name: Mapped[str]
    coffee_shop_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('coffee_shop.id'))
    coffee_shop: Mapped[CoffeeShop] = relationship(back_populates='owner')

class Coffee(Base):
    __tablename__ = 'coffees'

    id: Mapped[_id]
    name: Mapped[str]
    price: Mapped[int]
    coffee_shop: Mapped['CoffeeShop'] = relationship(back_populates="coffees")


class User(Base):
    __tablename__ = 'users'

    id: Mapped[_id]
    name: Mapped[str]
    age: Mapped[int]
    favorite_coffee: Mapped['Coffee']