from typing import Annotated

import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column

from database import Base

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]

class Film(Base):
    __tablename__ = 'Film'
    id: Mapped[_id]
    name: Mapped[str]
    directors: Mapped[str]
