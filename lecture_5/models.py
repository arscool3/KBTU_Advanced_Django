from typing import Annotated
from datetime import date

import sqlalchemy
from sqlalchemy.orm import Session, Mapped, mapped_column, relationship
from database import Base

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]

class Country(Base):
    __tablename__ = 'Country'

    id: Mapped[_id]
    name: Mapped[str]
    created_at: Mapped[date]
    president: Mapped["President"] = relationship(back_populates='country')


class President(Base):
    __tablename__ = 'Presidents'

    id: Mapped[_id]
    name: Mapped[str]
    country_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('Country.id'))
    country: Mapped[Country]= relationship(back_populates='president')


class Citizen(Base):
    __tablename__ = 'Persons'
    id: Mapped[_id]
    name: Mapped[str]