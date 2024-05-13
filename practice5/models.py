from typing import Annotated

import sqlalchemy
from sqlalchemy.orm import mapped_column, Mapped, relationship  

from database import Base

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]

class Cinema(Base):
    id: Mapped[_id]
    name: Mapped[str]

class Genre(Cinema):
    __tablename__ = 'genres'
    film: Mapped['Film'] = relationship('genres')

class Director(Cinema):
    __tablename__ = 'directors'
    film: Mapped['Film'] = relationship('directors')


class Film(Cinema):
    __tablename__ = 'films'
    film: Mapped['Film'] = relationship('films')