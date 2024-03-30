from typing import Annotated

import sqlalchemy
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.ext.declarative import declarative_base

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]
Base = declarative_base()

class FilmModel(Base):
    __tablename__ = "films"
    id: Mapped[_id]
    name: Mapped[str]
    director: Mapped[str]
