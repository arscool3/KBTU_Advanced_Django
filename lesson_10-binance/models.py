from datetime import datetime

from sqlalchemy import String, Float, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from db import Base


class Bitcoin(Base):
    __tablename__ = 'bitcoins'

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(Float)
    start_date: Mapped[str] = mapped_column(String)
    end_date: Mapped[str] = mapped_column(String)