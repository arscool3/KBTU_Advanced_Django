from typing import Annotated

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, Mapped, mapped_column
from datetime import date

url = 'postgresql://postgres:postgres@localhost:5433/postgres'
engine = create_engine(url)
session = Session(engine)
Base = declarative_base()

_id = Annotated[str, mapped_column(sqlalchemy.Integer, primary_key=True)]


class Teacher(Base):
    __tablename__ = 'teachers'

    id: Mapped[_id]
    name: Mapped[str]
    yoe: Mapped[int]


class Student(Base):
    __tablename__ = 'students'

    id: Mapped[_id]
    name: Mapped[str]
    year: Mapped[int]


class Lesson(Base):
    __tablename__ = 'lessons'

    id: Mapped[_id]
    title: Mapped[str]
    date: Mapped[date]
