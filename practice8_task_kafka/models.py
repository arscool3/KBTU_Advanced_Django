from typing import Annotated

import sqlalchemy
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]


class Film(Base):
    __tablename__ = "film"

    id: Mapped[_id]

    name: Mapped[str]
    director: Mapped[str]