from typing import Annotated
import sqlalchemy
from sqlalchemy.orm import mapped_column, relationship, Mapped
from database import Base

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]


class Message(Base):
    __tablename__ = 'message'
    id: Mapped[_id]
    name: Mapped[str]
    name: Mapped[str]