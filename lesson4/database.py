from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped

url = 'postgresql://postgres:Haker15987@postgres/postgres'
engine = create_engine(url)

Base = declarative_base()


class Teacher(Base):
    name: Mapped[str]
    yoe: Mapped[int]


class Student(Base):
    name: Mapped[str]
    age: Mapped[int]

