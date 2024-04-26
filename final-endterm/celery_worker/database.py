import os
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, Mapped, mapped_column, relationship
from typing import Annotated

url = os.environ.get("POSTGRES_URL", "postgresql://postgres:postgres@localhost/postgres")
engine = create_engine(url)

session = Session(engine)

Base = declarative_base()

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]


class History(Base):
    __tablename__ = "history"
    id: Mapped[_id]
    timestamp: Mapped[int]
    person_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("people.id"))
    location_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("locations.id"))


class Person(Base):
    __tablename__ = "people"
    id: Mapped[_id]
    current_location: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("locations.id"))
    history = relationship("History", back_populates="person")


class Position(Base):
    __tablename__ = "positions"
    id: Mapped[_id]
    latitude: Mapped[float]
    longitude: Mapped[float]
    roads = relationship("Road", back_populates="start_position")


class Location(Base):
    __tablename__ = "locations"
    id: Mapped[_id]
    latitude: Mapped[float]
    longitude: Mapped[float]
    people = relationship("Person", back_populates="current_location")


class Road(Base):
    __tablename__ = "roads"
    id: Mapped[_id]
    name: Mapped[str]
    region: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("regions.id"))
    traffic_rate: Mapped[float] = 0.0
    # must be a rectangle
    start_position: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("positions.id"))
    end_position: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("positions.id"))


class Region(Base):
    __tablename__ = "regions"
    id: Mapped[_id]
    name: Mapped[str]
    roads = relationship("Road", back_populates="region")
