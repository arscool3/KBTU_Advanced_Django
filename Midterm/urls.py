from typing import Optional

import models
from fastapi import APIRouter, Depends, HTTPException
from dependencies import *
from sqlalchemy import select
from schemas import *


router = APIRouter(prefix="")


@router.post("/hooper/", tags=['hoopers'])
def create_hooper(hooper: CreateHooper, db: Database) -> str:
    db.add(models.Hooper(hooper.model_dump()))
    return hooper.name


@router.get("/hoopers/", tags=["hoopers"])
def get_hoopers(db: Database) -> list[Hooper]:
    db_hoopers = db.query(models.Hooper).scalars()
    return list(map(Hooper.model_validate, db_hoopers))


@router.delete("/hoopers/", tags=["hoopers"])
def delete_hooper(db: Database, hooper_id: int) -> bool:
    try:
        hooper = db.get(models.Hooper, id=hooper_id)
        db.delete(hooper)
        return True
    except:
        return False


@router.get("/hoopers/", tags=["hoopers"])
def get_hooper_by_id(hooper: HooperDependency) -> Optional[Hooper]:
    return hooper


@router.post('/commands/', tags=["commands"])
def create_command(command: CreateCommand, db: Database) -> bool:
    command_data = command.model_dump()
    db.add_command(command_data)
    return True


@router.get('/commands/', tags=["commands"])
def get_commands(db: Database) -> list[Command]:
    db_commands = db.query(models.Command).scalars()
    return list(map(Command.model_validate, db_commands))


@router.delete("/commands/", tags=["commands"])
def delete_command(command: CommandDependency) -> bool:
    command.delete()
    return True


@router.get("/commands/", tags=["commands"])
def get_command_by_id(command: CommandDependency) -> Optional[Command]:
    return command


@router.post("/conferences/", tags=["conferences"])
def create_conference(conference: CreateConference, db: Database) -> bool:
    db.add(models.Conference, conference.model_dump())
    return True


@router.delete("/conferences/", tags=["conferences"])
def delete_conference(conference: ConferenceDependency) -> bool:
    conference.delete()
    return True


@router.get("/conferences/", tags=["conferences"])
def get_conferences(db: Database) -> list[Conference]:
    db_conferences = db.query(models.Conference).scalars()
    return list(map(Conference.model_validate, db_conferences))


@router.get("/conferences/", tags=["conferences"])
def get_conference_by_id(conference: ConferenceDependency) -> Optional[Conference]:
    return conference

