from pydantic import BaseModel


class CreateMark(BaseModel):
    name: str


class CreatePerson(BaseModel):
    iin: str
    name: str
    surname: str


class CreateVehicle(BaseModel):
    mark_name: str
    name: str
    vin: str


class CreateLocation(BaseModel):
    latitude: float
    longitude: float


class CreateFine(BaseModel):
    fine_amount: int
    location: CreateLocation


class CreateInsurance(BaseModel):
    insurance_amount: int
