from fastapi import Depends
from sqlalchemy.orm import Session
from database import Patient, Doctor, Appointment, Availability, Heartbeat, session
from schemas import PatientCreate, DoctorCreate, AppointmentCreate, AvailabilityCreate, AppointmentConfirmation
from sqlalchemy import desc


def get_db():
    try:
        yield session
    finally:
        session.close()

def create_patient(db: Session, patient: PatientCreate):
    db_patient = Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def get_patient(db: Session, patient_id: int):
    return db.query(Patient).filter(Patient.id == patient_id).first()

def create_doctor(db: Session, doctor: DoctorCreate):
    db_doctor = Doctor(**doctor.dict())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

def get_doctor(db: Session, doctor_id: int):
    return db.query(Doctor).filter(Doctor.id == doctor_id).first()

def create_appointment(db: Session, appointment: AppointmentCreate):
    db_appointment = Appointment(**appointment.dict())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

def get_appointment(db: Session, appointment_id: int):
    return db.query(Appointment).filter(Appointment.id == appointment_id).first()

def create_availability(db: Session, availability: AvailabilityCreate):
    db_availability = Availability(**availability.dict())
    db.add(db_availability)
    db.commit()
    db.refresh(db_availability)
    return db_availability

def get_doctor_availability(db: Session, doctor_id: int):
    return db.query(Availability).filter(Availability.doctor_id == doctor_id).all()

def delete_appointment(db: Session, appointment_id: int) -> bool:
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if appointment:
        availability = db.query(Availability).filter(
            Availability.doctor_id == appointment.doctor_id,
            Availability.day_of_month == appointment.day_of_month,
            Availability.month == appointment.month,
            Availability.hour == appointment.hour
        ).first()
        if availability:
            db.delete(appointment)
            db.delete(availability)
            db.commit()
            return True
    return False

def process_appointment_confirmation(confirmation_data: AppointmentConfirmation):
    print(f"Received confirmation for appointment {confirmation_data.appointment_id}: {confirmation_data.confirmation_status}")

def insert_heartbeat_to_db(heartbeat: Heartbeat):
    db = session
    try: 
        db_heartbeat = Heartbeat(**heartbeat.dict())
        db.add(db_heartbeat)
        db.commit()
        # db.refresh(db_heartbeat)
    finally:
        db.close() 
    return db_heartbeat

def get_heartbeat_by_patient_id(patient_id: int):
    db = session
    heartbeat_data = []
    try: 
        heartbeat_data = db.query(Heartbeat).filter(Heartbeat.user_id == patient_id).all()
    finally:
        db.close() 
    return heartbeat_data