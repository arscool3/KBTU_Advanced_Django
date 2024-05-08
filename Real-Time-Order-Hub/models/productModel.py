from sqlalchemy import (
    Integer, String
)
import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column
from typing_extensions import Annotated
from database import Base


_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]


class Product(Base):
    __tablename__ = 'products'
    id: Mapped[_id]
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)