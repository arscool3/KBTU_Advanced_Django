import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Annotated

Base = declarative_base()

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True, autoincrement=True)]


class History(Base):
    __tablename__ = "history"
    id: Mapped[_id]
    timestamps = sqlalchemy.Column(sqlalchemy.DateTime(timezone=False))
    person_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("people.id"))
    person = relationship("Person", back_populates="history")
    location_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("locations.id"))


class Person(Base):
    __tablename__ = "people"
    login: Mapped[str] = mapped_column(sqlalchemy.String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(sqlalchemy.String, nullable=False)  # hashed
    id: Mapped[_id]
    current_location_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("locations.id"), nullable=True)
    current_location = relationship("Location", back_populates="people")
    current_road_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("roads.id"), nullable=True)
    current_road = relationship("Road", back_populates="people")
    history = relationship("History", back_populates="person")
    current_speed: Mapped[int] = mapped_column(sqlalchemy.Integer, default=0, insert_default=True, nullable=True)


class Position(Base):
    __tablename__ = "positions"
    id: Mapped[_id]
    latitude: Mapped[float]
    longitude: Mapped[float]
    # start_roads = relationship("Road", foreign_keys="[Road.start_position]")
    # end_roads = relationship("Road", foreign_keys="[Road.end_position]")


class Location(Base):
    __tablename__ = "locations"
    id: Mapped[_id]
    latitude: Mapped[float]
    longitude: Mapped[float]
    people = relationship("Person", back_populates="current_location")


class TrafficHistory(Base):
    __tablename__ = "traffic_history"
    id: Mapped[_id]
    timestamp = sqlalchemy.Column(sqlalchemy.DateTime(timezone=False))
    road_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("roads.id"))
    average_speed: Mapped[int]
    traffic_rate: Mapped[int]
    road = relationship("Road", back_populates="history")


class Road(Base):
    __tablename__ = "roads"
    id: Mapped[_id]
    name: Mapped[str]
    region_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("regions.id"))
    region = relationship("Region", back_populates="roads")
    traffic_rate: Mapped[float] = mapped_column(sqlalchemy.Float, default=0.0, insert_default=True)
    # must be a rectangle
    start_position: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("positions.id"))
    end_position: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("positions.id"))
    max_speed: Mapped[int] = mapped_column(sqlalchemy.Integer, default=60, insert_default=True)
    average_speed: Mapped[int] = mapped_column(sqlalchemy.Integer, default=0, insert_default=True)
    max_num_of_cars: Mapped[int] = mapped_column(sqlalchemy.Integer, default=50, insert_default=True)
    history = relationship("TrafficHistory", back_populates="road")
    people = relationship("Person", back_populates="current_road")


class Region(Base):
    __tablename__ = "regions"
    id: Mapped[_id]
    name: Mapped[str]
    roads = relationship("Road", back_populates="region")
