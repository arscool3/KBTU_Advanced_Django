import models
from fastapi import APIRouter, Depends, HTTPException
from dependecies import *
from sqlalchemy import select
from schemas import (Mark, CreateMark, CreatePerson, Person, Vehicle, CreateVehicle, CreateFine, OnlyFine, OnlyLocation,
                     CreateInsurance, PersonInsurance)

router = APIRouter(prefix="")


@router.post("/marks/", tags=["marks"])
def create_mark(mark: CreateMark, db: Database) -> str:
    db.add(models.Mark(**mark.model_dump()))
    return mark.name


@router.get("/marks/", tags=["marks"])
def get_marks_list(db: Database) -> list[Mark]:
    db_marks = db.execute(select(models.Mark)).scalars()
    return [Mark.model_validate(db_mark) for db_mark in db_marks]


@router.delete("/marks/", tags=["marks"])
def remove_mark(db: Database, mark_id: int) -> str:
    mark = db.get(models.Mark, mark_id)
    db.delete(mark)
    return "Deleted"


@router.post("/person/", tags=["people"])
def create_person(person: CreatePerson, db: Database) -> str:
    db.add(models.Person(**person.model_dump()))
    return person.iin


@router.get("/person/", tags=["people"])
def get_person_by_iin(person: PersonDependency) -> Person:
    return person


@router.delete("/person/", tags=["people"])
def remove_person(db: Database, iin: str) -> str:
    person = db.get(models.Person, iin)
    db.delete(person)
    return "Deleted"


@router.post("/vehicle/", tags=["vehicles"])
def create_vehicle(vehicle: CreateVehicle, db: Database, person: PersonDependency) -> str:
    vehicle_data = vehicle.model_dump()
    mark_name = vehicle_data.pop("mark_name")
    mark_id = db.execute(select(models.Mark).where(models.Mark.name == mark_name)).scalars().first().id
    vehicle_data["mark_id"] = mark_id

    vehicle_data["owner_id"] = person.iin

    db.add(models.Vehicle(**vehicle_data))
    return vehicle.vin


@router.get("/vehicle/", tags=["vehicles"])
def get_vehicle_by_vin(vehicle: VehicleDependency) -> Vehicle:
    return vehicle


@router.delete("/vehicle/", tags=["vehicles"])
def remove_person(db: Database, vin: str) -> str:
    db_vehicle = db.execute(select(models.Vehicle).where(models.Vehicle.vin == vin)).scalars().first()
    db.delete(db_vehicle)
    return "Deleted"


@router.post("/fines/add/", tags=["fines"])
def add_fine_vin(fine_data: CreateFine, vehicle: VehicleDependency, db: Database) -> str:
    fine_data = fine_data.model_dump()
    location_data = fine_data.pop("location")
    location = models.Location(**location_data)
    db.add(location)
    fine_data["location"] = location
    fine_data["fined_person_id"] = vehicle.owner.iin
    fine_data["fined_vehicle_id"] = vehicle.id

    fine = models.Fine(**fine_data)
    db.add(fine)
    return "Added fine for {}, amount: {}".format(vehicle.owner.iin, fine_data["fine_amount"])


@router.get("/fines/iin/", tags=["fines"])
def list_all_fines_by_person(person: PersonDependency) -> list[OnlyFine]:
    return person.fines


@router.get("/fines/iin/locations/", tags=["fines"])
def list_all_fines_locations_by_person(person: PersonDependency) -> list[OnlyLocation]:
    return [fine.location for fine in person.fines]


@router.delete("/fines/iin/remove/", tags=["fines"])
def remove_fine_from_person(db: Database, person: PersonDependency, fine_id: int) -> str:
    fines_ids = [fine.id for fine in person.fines]
    if fine_id in fines_ids:
        fine = db.get(models.Fine, fine_id)
        db.delete(fine)
        return "Deleted fine from {}".format(person.iin)
    else:
        raise HTTPException(status_code=400, detail="No such fine for that person")


@router.post("/insurance/add/", tags=["insurances"])
def add_insurance(
        insurance_data: CreateInsurance,
        vehicle: ModelVehicleDependency,
        person: ModelPersonDependency,
        db: Database
) -> str:
    insurance = models.Insurance(**insurance_data.model_dump())
    insurance.vehicles.append(vehicle)
    insurance.people.append(person)
    db.add(insurance)
    return "Added insurance for {}, vin: {}".format(vehicle.owner_id, vehicle.vin)


@router.get("/insurance/iin/", tags=["insurances"])
def list_all_insurances_person_in(person: PersonDependency) -> list[PersonInsurance]:
    return person.insurances


@router.patch("/insurance/iin/remove/", tags=["insurances"])
def remove_person_from_insurance(db: Database, person: ModelPersonDependency, insurance_id: int) -> str:
    insurance = db.get(models.Insurance, insurance_id)
    insurance.people.remove(person)
    return "Removed"
