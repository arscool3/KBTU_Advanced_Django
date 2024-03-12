from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base


class Owner(Base):
    __tablename__ = "owners"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    cars = relationship("Car", back_populates="owner")


class Car(Base):
    __tablename__ = "cars"
    id = Column(Integer, primary_key=True, index=True)
    vin = Column(String, unique=True, index=True)
    plate = Column(String, unique=True, index=True)
    model = Column(String, index=True)
    year = Column(Integer, index=True)
    owner_id = Column(Integer, ForeignKey("owners.id"))
    owner = relationship("Owner", back_populates="cars")

