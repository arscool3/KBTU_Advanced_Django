from typing import Annotated
import sqlalchemy
from sqlalchemy import String, Float, Column, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]


# class BitcoinCreate(Base):
#     __tablename__ = 'bitcoins'
#
#     id: Mapped[_id]
#     name: Mapped[str] = mapped_column(String)
#     price: Mapped[float] = mapped_column(Float)
#     start_date: Mapped[str] = mapped_column(String)
#     end_date: Mapped[str] = mapped_column(String)
#
#     def __init__(self, name, price, start_date, end_date):
#         self.name = name
#         self.price = price
#         self.start_date = start_date
#         self.end_date = end_date

class BaseBitcoin(Base):
    __tablename__ = 'bitcoins'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Float)
    start_date = Column(DateTime)
    end_date = Column(DateTime)