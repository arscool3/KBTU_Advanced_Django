from datetime import date
from typing import Annotated

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship

Base = declarative_base()
_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]


class Country(Base):
    __tablename__ = "country"

    id: Mapped[_id]
    name: Mapped[str]
    created_at: Mapped[date] = mapped_column(sqlalchemy.DATE, default=date.today())
    president: Mapped['President'] = relationship(back_populates="country")


class President(Base):
    __tablename__ = "president"

    id: Mapped[_id]
    name: Mapped[str]
    country_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("country.id"))
    country: Mapped[Country] = relationship(back_populates="president")


class Citizen(Base):
    __tablename__ = "citizen"

    id: Mapped[_id]
    name: Mapped[str]
    age: Mapped[int]


