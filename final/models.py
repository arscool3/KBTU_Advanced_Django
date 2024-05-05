from sqlalchemy import Column, Integer, String, Text, Enum, Date, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import List, Optional

Base = declarative_base()

association_table = Table('association', Base.metadata,
    Column('adoption_application_id', Integer, ForeignKey('adoption_applications.id')),
    Column('pet_id', Integer, ForeignKey('pets.id'))
)

class Pet(Base):
    __tablename__ = 'pets'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    species = Column(String, index=True)
    breed = Column(String, index=True)
    age = Column(Integer)
    gender = Column(Enum('male', 'female', 'unknown'), index=True)
    size = Column(Enum('small', 'medium', 'large', 'unknown'), index=True)
    color = Column(String)
    personality_traits = Column(Text)
    medical_history = Column(Text)
    vaccination_status = Column(String)
    spaying_neutering_status = Column(String)
    special_needs = Column(Text)
    
    adoption_applications = relationship("AdoptionApplication", secondary=association_table, back_populates="pets")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    location = Column(String)
    preferred_species = Column(String)
    preferred_age_range = Column(String)
    
    adoption_applications = relationship("AdoptionApplication", back_populates="user")


class AdoptionApplication(Base):
    __tablename__ = 'adoption_applications'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    status = Column(Enum('pending', 'approved', 'rejected'), default="pending")
    application_details = Column(Text)
    
    user = relationship("User", back_populates="adoption_applications")
    pets = relationship("Pet", secondary=association_table, back_populates="adoption_applications")


class AdoptionEvent(Base):
    __tablename__ = 'adoption_events'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)
    date = Column(Date)
    description = Column(Text)
    
    participating_organizations = relationship("ShelterRescue", secondary="event_shelter_rescue_association")


class ShelterRescue(Base):
    __tablename__ = 'shelters_rescues'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    contact_information = Column(String)
    location = Column(String)
    mission_statement = Column(Text)
    available_services = Column(Text)
    
    events_participated = relationship("AdoptionEvent", secondary="event_shelter_rescue_association")


class EventShelterRescueAssociation(Base):
    __tablename__ = 'event_shelter_rescue_association'

    event_id = Column(Integer, ForeignKey('adoption_events.id'), primary_key=True)
    shelter_rescue_id = Column(Integer, ForeignKey('shelters_rescues.id'), primary_key=True)
