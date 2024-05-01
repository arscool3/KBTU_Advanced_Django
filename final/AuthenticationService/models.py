import uuid

from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Customer(Base):
    __tablename__ = 'users'

    id: Mapped[str] = mapped_column(primary_key=True, default=str(uuid.uuid4()))
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    phone_number: Mapped[str] = mapped_column(nullable=False)
    address: Mapped[str]
    hashed_password: Mapped[str] = mapped_column(nullable=False)