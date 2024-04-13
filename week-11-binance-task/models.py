from datetime import datetime

from sqlalchemy import String, Float, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from database import Base

class Bitcoin(Base):
    __tablename__ = 'bitcoin'

    id: Mapped[str] = mapped_column(String, primary_key=True)
    time: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    price: Mapped[float] = mapped_column(Float)
    coin: Mapped[str] = mapped_column(String)