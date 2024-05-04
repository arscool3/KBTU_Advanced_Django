from sqlalchemy import String, BigInteger
import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column
from typing_extensions import Annotated
from database import Base


_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]


class User(Base):
    __tablename__ = "users"
    id: Mapped[_id]
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    phone_number: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    address: Mapped[str] = mapped_column(String, nullable=False)


class UserChatID(Base):
    __tablename__ = 'user_chat_ids'
    id: Mapped[_id]
    chat_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False)


