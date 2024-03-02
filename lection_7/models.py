from datetime import date
from typing import Annotated

import sqlalchemy
from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]

union_country_table = sqlalchemy.Table(
    "association",
    Base.metadata,
    sqlalchemy.Column("union_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("unions.id")),
    sqlalchemy.Column("country_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("countries.id")),
)


# Country <-> President one to one
# Country <-> Citizen - One to Many
class Country(Base):
    __tablename__ = "countries"

    id: Mapped[_id]
    name: Mapped[str]
    created_at: Mapped[date] = mapped_column(sqlalchemy.DATE, default=date.today())
    president: Mapped["President"] = relationship(back_populates="country")
    citizens: Mapped[list["Citizen"]] = relationship(back_populates="country")
    unions: Mapped[list["Union"]] = relationship(secondary=union_country_table, back_populates="countries")


class President(Base):
    __tablename__ = "presidents"

    id: Mapped[_id]
    name: Mapped[str]
    country_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("countries.id"))
    country: Mapped[Country] = relationship(back_populates="president")


class Citizen(Base):
    __tablename__ = "citizens"

    id: Mapped[_id]
    name: Mapped[str]
    age: Mapped[int]
    country_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("countries.id"))
    country: Mapped[Country] = relationship(back_populates="citizens")


class Union(Base):
    __tablename__ = "unions"

    id: Mapped[_id]
    name: Mapped[str]
    countries: Mapped[list[Country]] = relationship(secondary=union_country_table, back_populates="unions")
