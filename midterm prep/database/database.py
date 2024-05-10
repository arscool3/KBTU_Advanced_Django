from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from dotenv import dotenv_values

from typing import Annotated
from datetime import date

import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship, sessionmaker


config = dotenv_values(".env")

url = 'postgresql://{user}:{password}@localhost:5428/{database}'.format(
    user=config.get("POSTGRES_USER"),
    password=config.get("POSTGRES_PASSWORD"),
    database=config.get("POSTGRES_DB")
)

engine = create_engine(url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

association_table = Table('association', Base.metadata,
    Column('coffee_shop_id', Integer, ForeignKey('coffee_shops.id')),
    Column('coffee_id', Integer, ForeignKey('coffees.id'))
)

class CoffeeShop(Base):
    __tablename__ = 'coffee_shops'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    rating = Column(Integer)
    
    owner_id = Column(Integer, ForeignKey('coffee_shop_owners.id'))
    owner = relationship("CoffeeShopOwner", back_populates='coffee_shops')
    
    coffees = relationship("Coffee", secondary=association_table, back_populates='coffee_shops')

class CoffeeShopOwner(Base):
    __tablename__ = 'coffee_shop_owners'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    coffee_shops = relationship("CoffeeShop", back_populates='owner')

class Coffee(Base):
    __tablename__ = 'coffees'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)  # Описание кофе, если нужно
    price = Column(Integer)  # Цена кофе, если нужно
    
    coffee_shops = relationship("CoffeeShop", secondary=association_table, back_populates='coffees')

# class CoffeeShop(Base):
#     __tablename__ = 'coffe_shops'

#     id: Mapped[_id]
#     name: Mapped[str]
#     rating: Mapped[int]
#     owner_id = Column(Integer, ForeignKey('coffee_shop_owners.id'))

#     owner: Mapped['CoffeeShopOwner'] = relationship("CoffeeShopOwner", back_populates='coffee_shop')
#     coffees: Mapped['Coffee'] = relationship("Coffee", secondary=association_table, back_populates='coffee_shops')


# class CoffeeShopOwner(Base):
#     __tablename__ = 'coffee_shop_owners'

#     id: Mapped[_id]
#     name: Mapped[str]
#     coffee_shop: Mapped['CoffeeShop'] = relationship(back_populates='owner')

# class Coffee(Base):
#     __tablename__ = 'coffees'

#     id: Mapped[_id]
#     name: Mapped[str]
#     price: Mapped[int]
#     coffee_shop: Mapped['CoffeeShop'] = relationship(back_populates="coffees")

#     coffee_shops = relationship("CoffeeShop", secondary=association_table, back_populates='coffees')


class User(Base):
    __tablename__ = 'users'

    id: Mapped[_id]
    name: Mapped[str]
    age: Mapped[int]
