import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, mapped_column, Mapped
from datetime import datetime
from typing import Annotated


url = 'postgresql://postgres:postgres@localhost/postgres'
engine = sqlalchemy.create_engine(url)
session = Session(engine)

Base = declarative_base()

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]

class Currency(Base):
    __tablename__ = 'currency'

    id: Mapped[_id]
    time: Mapped[datetime] = mapped_column(sqlalchemy.DateTime, default=datetime.now())
    price: Mapped[float]
    coin: Mapped[str]