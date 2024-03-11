from typing import Annotated
import sqlalchemy
from sqlalchemy.orm import mapped_column, Mapped, relationship

import product
from database import Base


_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]


class Cart(Base):
    __tablename__ = 'cart'
    id: Mapped[_id]
    user_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('user.id'))

    user = relationship('User', back_populates='cart')
    cart_items = relationship("CartItem", back_populates="cart")
