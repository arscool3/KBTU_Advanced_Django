from typing import Annotated
from core.database import Base
import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]

class Film(Base):
    __tablename__ = "films"

    id: Mapped[_id]
    name: Mapped[str]
    director: Mapped[str]
    