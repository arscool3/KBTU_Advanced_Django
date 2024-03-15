import sqlalchemy as sa

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, mapped_column, Mapped, relationship

from typing import Annotated

url = 'postgresql://postgres:JASIK_2004@localhost/adv_django_lec_5'
engine = sa.create_engine(url)
session = Session(engine)

Base = declarative_base()


def execute_session(obj):
    session.add(obj)
    session.commit()
    session.close()


_id = Annotated[int, mapped_column(sa.Integer, primary_key=True)]


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[_id]
    name: Mapped[Annotated[str, mapped_column(sa.String, unique=True)]]

    products: Mapped['Product'] = relationship(back_populates='category')


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[_id]
    name: Mapped[str]
    price: Mapped[int]
    rating: Mapped[float]
    category_id: Mapped[int] = mapped_column(sa.ForeignKey('categories.id'))

    category: Mapped[Category] = relationship(back_populates='products')
    orders: Mapped['Order'] = relationship(back_populates='product')


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[_id]
    completed: Mapped[bool]
    delivery_address: Mapped[str]
    product_id: Mapped[int] = mapped_column(sa.ForeignKey('products.id'))

    product: Mapped[Product] = relationship(back_populates='orders')
