from datetime import datetime
from typing import Annotated
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapped_column, Mapped

Base = declarative_base()

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]

class DataToHeatmap(Base):
    __tablename__ = 'bitcoin'
    id: Mapped[_id]
    start_time: Mapped[datetime]
    end_time: Mapped[datetime]
    name: Mapped[str] = mapped_column(default="Bitcoin")
    k_to_usd: Mapped[float]


