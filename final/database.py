from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship

url = "postgresql://postgres:postgres@localhost/postgres"

engine = create_engine(url)
session = Session(engine)

Base = declarative_base()

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String)

    appointments = relationship("Appointment", back_populates="patient")
    medical_records = relationship("MedicalRecord", back_populates="patient")

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    specialty = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String)

    availability = relationship("Availability", back_populates="doctor")
    appointments = relationship("Appointment", back_populates="doctor")

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    availability_id = Column(Integer, ForeignKey("availabilities.id"))
    appointment_datetime = Column(DateTime)
    status = Column(String)
    day_of_month = Column(Integer) 
    month = Column(Integer)         
    hour = Column(Integer)         

    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")
    medical_record = relationship("MedicalRecord", uselist=False, back_populates="appointment")
    payment = relationship("Payment", uselist=False, back_populates="appointment")
    availability = relationship("Availability", back_populates="appointment")

class Availability(Base):
    __tablename__ = "availabilities"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    day_of_month = Column(Integer) 
    month = Column(Integer)         
    hour = Column(Integer)          

    doctor = relationship("Doctor", back_populates="availability")
    appointment = relationship("Appointment", back_populates="availability")

class MedicalRecord(Base):
    __tablename__ = "medical_records"

    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id"))
    patient_id = Column(Integer, ForeignKey("patients.id"))
    diagnosis = Column(String)
    prescription = Column(String)

    patient = relationship("Patient", back_populates="medical_records")
    appointment = relationship("Appointment", back_populates="medical_record")

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id"))
    amount = Column(Float)
    payment_date = Column(DateTime)

    appointment = relationship("Appointment", back_populates="payment")

class Heartbeat(Base):
    __tablename__ = 'heartbeat'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True) 
    heart_rate = Column(Float)