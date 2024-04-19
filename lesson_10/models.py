from sqlalchemy import String, Float
from sqlalchemy.orm import mapped_column, Mapped
from typing_extensions import Annotated
import sqlalchemy
from db import Base

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]


class Bitcoin(Base):
    __tablename__ = 'bitcoins'

    id: Mapped[_id]
    name: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(Float)
    start_date: Mapped[str] = mapped_column(String)
    end_date: Mapped[str] = mapped_column(String)