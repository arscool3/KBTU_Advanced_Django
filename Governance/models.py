from datetime import date

import sqlalchemy
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database import Base

_id = mapped_column(sqlalchemy.Integer, primary_key=True)


class Country(Base):
    __tablename__ = 'countries'

    id: Mapped[_id]
    name: Mapped[str]
    created_at: Mapped[date] = mapped_column(sqlalchemy.DATE, default=date.today())
    president: Mapped['President'] = relationship(back_populates='country')


class President(Base):
    __tablename__ = 'presidents'

    id: Mapped[_id]
    name: Mapped[str]
    country_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('countries.id'))
    country: Mapped[Country] = relationship(back_populates='president')


class Citizen(Base):
    __tablename__ = 'citizens'

    id: Mapped[_id]
    name: Mapped[str]
    age: Mapped[int]
