from sqlalchemy.orm import Session, Mapped, mapped_column, relationship
from typing import Annotated
import sqlalchemy
from database import Base

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]



class Customer(Base):
    __tablename__ = 'customers'

    id: Mapped[_id]
    name: Mapped[str]
    
    cart: Mapped['Cart'] = relationship( back_populates='customer')


class Product(Base):
    __tablename__ = 'products'
    id: Mapped[_id]
    name: Mapped[str]
    price: Mapped[int]
    
    cartitem: Mapped['CartItem'] = relationship(back_populates='product')


class Cart(Base):
    __tablename__ = 'carts'

    id: Mapped[_id]

    customer_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('customers.id'))
    customer: Mapped[Customer] = relationship(back_populates='cart')

    cartitem: Mapped['CartItem'] = relationship(back_populates='cart')
    


class CartItem(Base):
    __tablename__ = 'cartitems'

    id: Mapped[_id]

    product_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('products.id'))
    product: Mapped[Product] = relationship(back_populates='cartitem')

    cart_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('carts.id'))
    cart : Mapped[Cart] = relationship(back_populates='cartitem')
    
    quantity: Mapped[int]