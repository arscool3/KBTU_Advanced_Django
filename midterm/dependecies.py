from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import Depends
from typing import Annotated
from database import get_db

import models
from schemas import *

__all__ = ("Database", "PersonDependency", "VehicleDependency", "ModelPersonDependency", "ModelVehicleDependency")

Database = Annotated[Session, Depends(get_db)]


def get_person_model(iin: str, db: Database) -> models.Person | None:
    db_person = db.get(models.Person, iin)
    return db_person


def get_vehicle_model(vin: str, db: Database) -> models.Vehicle | None:
    db_vehicle = db.execute(select(models.Vehicle).where(models.Vehicle.vin == vin)).scalars().first()
    if db_vehicle:
        return db_vehicle
    else:
        raise "Object 'Vehicle' with vin {} not found".format(vin)


class PersonDependencyClass:
    def __call__(self, db_person: models.Person = Depends(get_person_model)) -> Person:
        return Person.model_validate(db_person)


class VinVehicleDependencyClass:
    def __call__(self, db_vehicle: models.Vehicle = Depends(get_vehicle_model)) -> Vehicle:
        return Vehicle.model_validate(db_vehicle)


PersonDependency = Annotated[Person, Depends(PersonDependencyClass())]
VehicleDependency = Annotated[Vehicle, Depends(VinVehicleDependencyClass())]

ModelPersonDependency = Annotated[models.Person, Depends(get_person_model)]
ModelVehicleDependency = Annotated[models.Vehicle, Depends(get_vehicle_model)]
