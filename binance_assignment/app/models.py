from datetime import date, datetime
from typing import Annotated

import sqlalchemy
from sqlalchemy import Table, Column, Integer, ForeignKey

from sqlalchemy.orm import mapped_column, Mapped, relationship

from database import Base

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]


class BinanceDealModel(Base):
    __tablename__ = "binance_deals"
    id: Mapped[_id]
    symbol: Mapped[str]
    price: Mapped[float]
    quantity: Mapped[int]
    k_to_usd: Mapped[float]
    timestamp: Mapped[date] = mapped_column(sqlalchemy.DATE, default=date.today())
