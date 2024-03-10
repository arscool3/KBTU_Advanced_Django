from pydantic import BaseModel, field_serializer


class BaseClass(BaseModel):
    id: int

    class Config:
        from_attributes = True


class Mark(BaseClass):
    id: int
    name: str


class Person(BaseModel):
    iin: str
    name: str
    surname: str
    fines: list = []
    vehicles: list = []
    insurances: list = []

    class Config:
        from_attributes = True


class OnlyPerson(BaseModel):
    iin: str
    name: str
    surname: str

    class Config:
        from_attributes = True


class Vehicle(BaseClass):
    mark: Mark
    name: str
    vin: str
    owner: OnlyPerson
    fines: list = []
    insurances: list = []
