from typing import Annotated
import sqlalchemy
from sqlalchemy.orm import mapped_column, Mapped, relationship
from database import Base

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]


class CartItem(Base):
    __tablename__ = "cart_item"
    id: Mapped[_id]
    amount: Mapped[int] = mapped_column(default=1)

    product_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("product.id"))
    cart_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("cart.id"))

    product = relationship("Product", back_populates="cart_item")
    cart = relationship("cart_item", back_populates="cart_items")


