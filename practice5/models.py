# pip install fastapi uvicorn sqlalchemy alembic psycopg2-binary
from datetime import date
from typing import Annotated

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, Mapped, mapped_column, relationship

url = 'postgresql://postgres:aru@localhost/practice5'
engine = create_engine(url)
session = Session(engine)

Base = declarative_base()
_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]

class Citizen(Base):
    __tablename__='citizens'
    id:Mapped[_id]
    name:Mapped[str]
    age:Mapped[int]

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

