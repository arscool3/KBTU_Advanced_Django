from typing import Annotated

import sqlalchemy
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, Session, mapped_column, Mapped

Base = declarative_base()

url = url = 'postgresql://postgres:postgres@localhost:5438/postgres'
engine = create_engine(url)
session = Session(engine)
Base = declarative_base()


_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]

class Film(Base):
    __tablename__ = 'films'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    director = Column(String)

# Docker: e756cb9ea8ce0e6f98bce0846748c1bba0d9ead106d061679c22115cbea2ae06
