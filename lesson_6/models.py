from typing import Annotated
import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]


class Item(Base):
    __tablename__ = 'items'

    id: Mapped[_id]
    name: Mapped[str]
    description: Mapped[str]
    user_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('users.id'))
    user: Mapped['User'] = relationship('User', back_populates='items')
    categories: Mapped[list['Category']] = relationship(
        'Category', secondary='item_categories', back_populates='items')


class User(Base):
    __tablename__ = 'users'

    id: Mapped[_id]
    name: Mapped[str]
    email: Mapped[str]
    items: Mapped[list[Item]] = relationship('Item', back_populates='user')


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[_id]
    name: Mapped[str]
    items: Mapped[list[Item]] = relationship(
        'Item', secondary='item_categories', back_populates='categories')


class ItemCategory(Base):
    __tablename__ = 'item_categories'

    item_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('items.id'), primary_key=True)
    category_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('categories.id'), primary_key=True)
