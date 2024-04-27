from typing import Annotated
from datetime import date

import sqlalchemy
from sqlalchemy.orm import Session, Mapped, mapped_column, relationship
from lecture_7.database import Base

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]


class Cinema:
    id: Mapped[_id]
    name: Mapped[str]


class Genre(Cinema, Base):
    __tablename__ = "genres"
    films: Mapped[list["Genre"]] = relationship(back_populates="genre")


class Director(Cinema, Base):
    __tablename__ = "directors"
    films: Mapped[list["Film"]] = relationship(back_populates="director")


class Film(Cinema, Base):
    __tablename__ = "films"

    director_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("directors.id"))
    genre_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("genres.id"))
