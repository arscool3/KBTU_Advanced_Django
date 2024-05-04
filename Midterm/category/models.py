from typing import Annotated
import sqlalchemy
from sqlalchemy.orm import mapped_column, Mapped, relationship
from database import Base


_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]


class Category(Base):
    __tablename__ = "category"
    id: Mapped[_id]
    name: Mapped[str]
    description: Mapped[str] = mapped_column(nullable=True)

    products = relationship("Product", back_populates="category", cascade="all,delete")


