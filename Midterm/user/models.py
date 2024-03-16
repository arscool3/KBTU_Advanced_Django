from typing import Annotated
import sqlalchemy
from sqlalchemy.orm import mapped_column, Mapped, relationship
from database import Base
from cart.models import Cart

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]


class User(Base):
    __tablename__ = "user"
    id: Mapped[_id]
    name: Mapped[str]
    email: Mapped[str]

    cart = relationship(Cart, back_populates='user', uselist=False)