from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import PatientBase, PatientCreate, DoctorBase, DoctorCreate, AppointmentBase, AppointmentCreate, AvailabilityBase, AvailabilityCreate
from repositories import create_patient, get_patient, create_doctor, get_doctor, create_appointment, get_appointment, create_availability, get_doctor_availability, delete_appointment, get_heartbeat_by_patient_id
from database import session
from typing import List
import matplotlib.pyplot as plt
import numpy as np
from fastapi.responses import FileResponse

app = FastAPI()

def get_db():
    try:
        yield session
    finally:
        session.close()
    
class AvailabilityChecker:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def __call__(self, appointment: AppointmentCreate) -> bool:
        list_availability = read_doctor_availability(appointment.doctor_id, self.db)
        for availability in list_availability:
            if availability.day_of_month == appointment.day_of_month and \
               availability.month == appointment.month and \
               availability.hour == appointment.hour:
                return False
        return True

@app.post("/patients", response_model=PatientBase)
def create_patient_endpoint(patient: PatientCreate, db: Session = Depends(get_db)):
    return create_patient(db=db, patient=patient)

@app.get("/patients/{patient_id}", response_model=PatientBase)
def read_patient(patient_id: int, db: Session = Depends(get_db)):
    db_patient = get_patient(db=db, patient_id=patient_id)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient

@app.post("/doctors", response_model=DoctorBase)
def create_doctor_endpoint(doctor: DoctorCreate, db: Session = Depends(get_db)):
    return create_doctor(db=db, doctor=doctor)

@app.get("/doctors/{doctor_id}", response_model=DoctorBase)
def read_doctor(doctor_id: int, db: Session = Depends(get_db)):
    db_doctor = get_doctor(db=db, doctor_id=doctor_id)
    if db_doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return db_doctor

@app.post("/appointments")
def create_appointment_endpoint(appointment: AppointmentCreate, availability_checker: AvailabilityChecker = Depends()):
    if availability_checker(appointment):
        create_availability(db=availability_checker.db, availability=AvailabilityCreate(doctor_id=appointment.doctor_id,
                                                                                         day_of_month=appointment.day_of_month,
                                                                                         month=appointment.month,
                                                                                         hour=appointment.hour))
        return create_appointment(db=availability_checker.db, appointment=appointment)
    else:
        return {"message": "Doctor is not available at this time"}

@app.get("/doctor_availability/{doctor_id}", response_model=List[AvailabilityBase])
def read_doctor_availability(doctor_id: int, db: Session = Depends(get_db)):
    return get_doctor_availability(db=db, doctor_id=doctor_id)

@app.get("/appointments/{appointment_id}", response_model=AppointmentBase)
def read_appointment(appointment_id: int, db: Session = Depends(get_db)):
    db_appointment = get_appointment(db=db, appointment_id=appointment_id)
    if db_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return db_appointment


@app.delete("/appointments/{appointment_id}")
def delete_appointment_endpoint(appointment_id: int, db: Session = Depends(get_db)):
    if delete_appointment(db=db, appointment_id=appointment_id):
        return {"message": "Appointment deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Appointment not found")


# @app.post("/doctor_availability", response_model=AvailabilityBase)
# def create_doctor_availability(availability: AvailabilityCreate, db: Session = Depends(get_db)):
#     return create_availability(db=db, availability=availability)

@app.get("/heartbeat/{patient_id}")
async def get_patient_heartbeat(patient_id: int):
    heartbeat_data = get_heartbeat_by_patient_id(patient_id)
    return create_heartbeat_graph(heartbeat_data)

def create_heartbeat_graph(heartbeat_data):
    times = np.arange(1, len(heartbeat_data) + 1)

    # Extract heart rates
    heart_rates = [entry.heart_rate for entry in heartbeat_data]

    # Plot the graph
    plt.figure(figsize=(10, 6))
    plt.plot(times, heart_rates, linestyle='-')
    plt.title('Heartbeat Over Time')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Heart Rate')
    plt.grid(True)
    graph_file = "/tmp/heartbeat_graph.png"
    plt.savefig(graph_file)
    plt.close()
    return FileResponse(graph_file)