from typing import Annotated
from fastapi import FastAPI, Depends
from pydantic import BaseModel
import punq

class Patient(BaseModel):
    name: str
    age: int
    health_record: str

class Doctor(BaseModel):
    name: str
    specialty: str

class Appointment(BaseModel):
    patient_name: str
    doctor_name: str
    date: str

class HealthSubLayer:
    def __init__(self, log_message: str):
        self.log_message = log_message

    def add_patient(self, patient: Patient):
        print(self.log_message)

class HealthMainLayer:
    def __init__(self, repo: HealthSubLayer):
        self.repo = repo

    def add_patient(self, patient: Patient) -> str:
        print("Adding Patient")
        self.repo.add_patient(patient)
        print("Patient Added")
        return "Patient was added"

def get_container() -> punq.Container:
    container = punq.Container()
    container.register(HealthSubLayer, instance=HealthSubLayer(log_message='Adding Patient to System'))
    container.register(HealthMainLayer)
    return container

app = FastAPI()
doctors = []
appointments = []

def add_doctor(doctor: Doctor) -> str:
    doctors.append(doctor)
    return "Doctor added"

def add_appointment(appointment: Appointment) -> str:
    appointments.append(appointment)
    return "Appointment added"

@app.post("/patients")
def add_patient(patient: Annotated[Patient, Depends(get_container().resolve(HealthMainLayer).add_patient)]) -> str:
    return patient

@app.post("/doctors")
async def add_doctor_endpoint(doctor: Annotated[Doctor, Depends(add_doctor)]):
    return doctor

@app.post("/appointments")
async def add_appointment_endpoint(appointment: Annotated[Appointment, Depends(add_appointment)]):
    return appointment

@app.get("/doctors")
async def get_doctors() -> list[Doctor]:
    return doctors

@app.get("/appointments")
async def get_appointments() -> list[Appointment]:
    return appointments
