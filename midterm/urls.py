import models
from fastapi import APIRouter, Depends
from dependecies import Database
from sqlalchemy import select
from schemas import Mark, CreateMark, CreatePerson, Person, Vehicle, CreateVehicle

router = APIRouter(prefix="")


@router.post("/marks/", tags=["marks"])
def create_mark(mark: CreateMark, db: Database):
    db.add(models.Mark(**mark.model_dump()))
    return mark.name


@router.get("/marks/", tags=["marks"])
def get_marks_list(db: Database) -> list[Mark]:
    db_marks = db.execute(select(models.Mark)).scalars()
    return [Mark.model_validate(db_mark) for db_mark in db_marks]


@router.post("/person/", tags=["people"])
def create_person(person: CreatePerson, db: Database):
    db.add(models.Person(**person.model_dump()))
    return person.iin


@router.get("/person/", tags=["people"])
def get_person_by_iin(db: Database, iin: str) -> Person:
    db_person = db.get(models.Person, iin)
    return Person.model_validate(db_person)


@router.post("/vehicle/", tags=["vehicles"])
def create_vehicle(vehicle: CreateVehicle, db: Database, person=Depends(get_person_by_iin)):
    vehicle_data = vehicle.model_dump()
    mark_name = vehicle_data.pop("mark_name")
    mark_id = db.execute(select(models.Mark).where(models.Mark.name == mark_name)).scalars().first().id
    vehicle_data["mark_id"] = mark_id

    vehicle_data["owner_id"] = person.iin

    db.add(models.Vehicle(**vehicle_data))
    return vehicle.vin


@router.get("/vehicle/", tags=["vehicles"])
def get_vehicle_by_vin(db: Database, vin: str) -> Vehicle:
    db_vehicle = db.execute(select(models.Vehicle).where(models.Vehicle.vin == vin)).scalars().first()
    if db_vehicle:
        return Vehicle.model_validate(db_vehicle)
    else:
        print("HERE")
        return "Object 'Vehicle' with vin {} not found".format(vin)
