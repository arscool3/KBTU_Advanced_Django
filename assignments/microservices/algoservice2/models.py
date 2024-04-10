from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class Data(Base):
    __tablename__ = 'data'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    time: Mapped[str] = mapped_column(default=datetime.now())
    name: Mapped[str] = mapped_column(nullable=False)
    correlation_coefficient: Mapped[float] = mapped_column(nullable=False)
