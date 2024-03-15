from typing import Annotated

import sqlalchemy as sa

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship

url = 'postgresql://postgres:postgres@localhost/postgres'
engine = create_engine(url)
session = Session(engine)

Base = declarative_base()
_id = Annotated[int, mapped_column(sa.INTEGER, primary_key=True)]


class Country(Base):
    __tablename__ = 'countries'
    id: Mapped[_id]
    name: Mapped[str]
    president: Mapped['President'] = relationship(back_populates='country')


class President(Base):
    __tablename__ = 'presidents'
    id: Mapped[_id]
    name: Mapped[str]
    country_id: Mapped[int] = mapped_column(sa.ForeignKey('countries.id'))
    country: Mapped[Country] = relationship(back_populates='president')