from pydantic import BaseModel
from datetime import datetime

class PatientBase(BaseModel):
    name: str
    email: str
    phone: str

class PatientCreate(PatientBase):
    pass

class DoctorBase(BaseModel):
    name: str
    specialty: str
    email: str
    phone: str

class DoctorCreate(DoctorBase):
    pass

class AppointmentBase(BaseModel):
    # appointment_datetime: datetime
    patient_id: int
    doctor_id: int
    day_of_month: int
    month: int 
    hour: int 

class AppointmentCreate(AppointmentBase):
    patient_id: int
    doctor_id: int
    day_of_month: int
    month: int 
    hour: int 


class AvailabilityBase(BaseModel):
    day_of_month: int
    month: int
    hour: int

class AvailabilityCreate(AvailabilityBase):
    doctor_id: int


class MedicalRecordBase(BaseModel):
    diagnosis: str
    prescription: str

class MedicalRecordCreate(MedicalRecordBase):
    appointment_id: int

class PaymentBase(BaseModel):
    amount: float
    payment_date: datetime

class PaymentCreate(PaymentBase):
    appointment_id: int

class AppointmentConfirmation(BaseModel):
    appointment_id: int
    confirmation_status: str
    additional_details: str = None
    confirmed_at: datetime = datetime.now()

class Heartbeat(BaseModel):
    user_id: int
    heart_rate: int

    class Config:
        from_attributes = True