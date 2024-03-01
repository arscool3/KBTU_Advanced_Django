from typing import Annotated
from datetime import date

import sqlalchemy
from sqlalchemy.orm import Session, Mapped, mapped_column, relationship
from database import Base

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]


class Human(Base):
    __tablename__ = 'Human'

    id: Mapped[_id]
    name: Mapped[str]
    birth_day: Mapped[date]


class Dog(Base):
    __tablename__ = 'Dog'

    id: Mapped[_id]
    name: Mapped[str]
    human: Mapped[Human] = relationship(back_populates='dog')


class Cat(Base):
    __tablename__ = 'Cat'
    id: Mapped[_id]
    name: Mapped[str]
    human: Mapped[Human] = relationship(back_populates='cat')


class House(Base):
    __tablename__ = 'House'
    id: Mapped[_id]
    address: Mapped[str]
    owner: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('Human.id'))
    cats: Mapped[Cat] = relationship(back_populates='house')
    dogs: Mapped[Dog] = relationship(back_populates='house')
