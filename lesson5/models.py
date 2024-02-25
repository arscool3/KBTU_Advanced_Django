import sqlalchemy
from datetime import date
from typing import Annotated
from sqlalchemy.orm import Mapped, mapped_column, declarative_base

Base = declarative_base()
_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]


class Country(Base):
    __tablename__ = 'countries'

    id: Mapped[_id]
    name: Mapped[str]
    created_at: Mapped[date] = mapped_column(sqlalchemy.DATE, default=date.today())


class President(Base):
    __tablename__ = 'presidents'

    id: Mapped[_id]
    name: Mapped[str]


class Citizen(Base):
    __tablename__ = 'citizens'

    id: Mapped[_id]
    name: Mapped[str]
    age: Mapped[int]

