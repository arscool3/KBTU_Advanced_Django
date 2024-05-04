from typing import Annotated
import sqlalchemy
from sqlalchemy.orm import mapped_column, Mapped, relationship
from database import Base

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]


class Product(Base):
    __tablename__ = "product"
    id: Mapped[_id]
    name: Mapped[str]
    description: Mapped[str] = mapped_column(nullable=True)
    price: Mapped[float]
    amount: Mapped[int]
    category_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("category.id"))
    firm_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("firm.id"))

    # category = relationship("Category", back_populates="products")
    category = relationship("Category", back_populates="products", lazy='select')
    firm = relationship("Firm", back_populates='products')
    cart_item = relationship("CartItem", back_populates="product")
    # analys_product = relationship("PopularProduct", back_populates="product")
