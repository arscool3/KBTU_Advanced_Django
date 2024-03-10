from pydantic import BaseModel, field_serializer


class BaseClass(BaseModel):
    id: int

    class Config:
        from_attributes = True


class Mark(BaseClass):
    id: int
    name: str


class OnlyVehicle(BaseClass):
    mark: Mark
    name: str
    vin: str


class OnlyLocation(BaseClass):
    latitude: float
    longitude: float


class OnlyFine(BaseClass):
    fined_vehicle: OnlyVehicle
    fine_amount: int
    location: OnlyLocation


class PersonInsurance(BaseClass):
    insurance_amount: int
    vehicles: list[OnlyVehicle]


class Person(BaseModel):
    iin: str
    name: str
    surname: str
    fines: list[OnlyFine] = []
    vehicles: list[OnlyVehicle] = []
    insurances: list[PersonInsurance] = []

    class Config:
        from_attributes = True


class OnlyPerson(BaseModel):
    iin: str
    name: str
    surname: str

    class Config:
        from_attributes = True


class VehicleFine(BaseClass):
    fined_person: OnlyPerson
    fine_amount: int
    location: OnlyLocation


class VehicleInsurance(BaseClass):
    insurance_amount: int
    people: list[OnlyPerson]


class Vehicle(BaseClass):
    mark: Mark
    name: str
    vin: str
    owner: OnlyPerson
    fines: list[VehicleFine] = []
    insurances: list[VehicleInsurance] = []
