import sqlalchemy as sa

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, Session, mapped_column

url = 'postgresql://postgres:postgres@localhost:5433/postgres'
engine = create_engine(url)
session = Session(engine)

Base = declarative_base()


class Teacher(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(sa.INTEGER, primary_key=True)
    name: Mapped[str]
    years: Mapped[int]


class Student(Base):
    __tablename__ = 'students'

    id: Mapped[int] = mapped_column(sa.INTEGER, primary_key=True)
    name: Mapped[str]
    age: Mapped[int]

