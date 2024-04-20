from typing import Annotated
from core.database import Base
import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]


class HeatMapData(Base):
    __tablename__ = "heat_map_data"
    id: Mapped[_id]
    time: Mapped[datetime]
    data = mapped_column(sqlalchemy.JSON)