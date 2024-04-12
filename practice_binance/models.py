from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from typing import Annotated
from sqlalchemy.orm import mapped_column, Mapped
import sqlalchemy

Base = declarative_base()

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]


class Price(Base):
    __tablename__ = 'prices'

    id = Mapped[_id]
    time = Mapped[datetime]
    name = Mapped[str]
    price = Mapped[float]
