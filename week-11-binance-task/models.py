from datetime import datetime
from typing import Annotated
import sqlalchemy
from sqlalchemy.orm import mapped_column, Mapped
from database import Base

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]


class Bitcoin(Base):
    __tablename__ = 'bitcoin'

    id: Mapped[_id]
    time: Mapped[datetime] = mapped_column(sqlalchemy.DateTime, default=datetime.now())
    price: Mapped[float]
    coin: Mapped[str]
