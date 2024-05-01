from __future__ import annotations
from typing import Optional

from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

import models
from database import get_db
from schemas import Hooper, Command, Conference

__all__ = (
    "Database",
    "HooperDependency",
    "CommandDependency",
    "ModelHooperDependency",
    "ModelCommandDependency",
    "ConferenceDependency",
    "ModelConferenceDependency",
)

Database = Annotated[Session, Depends(get_db)]


def get_hooper_model(hooper_id: int, db: Database) -> Optional[models.Hooper]:
    db_hooper = db.get(models.Hooper, hooper_id)
    return db_hooper


def get_command_model(command_id: int, db: Database) -> Optional[models.Command]:
    db_command = db.get(models.Command, command_id)
    return db_command


def get_conference_model(conference_id: int, db: Database) -> Optional[models.Conference]:
    return db.get(models.Conference, conference_id)


class HooperDependencyClass:
    def __call__(self, db_hooper: models.Hooper = Depends(get_hooper_model)) -> Optional[Hooper]:
        return Hooper.model_validate(db_hooper)


class CommandDependencyClass:
    def __call__(self, db_command: models.Command = Depends(get_command_model)) -> Optional[Command]:
        return Command.model_validate(db_command)


class ConferenceDependencyClass:
    def __call__(self, db_conference: models.Conference = Depends(get_conference_model)) -> Optional[
        Conference]:
        return Conference.model_validate(db_conference)


HooperDependency = Annotated[Hooper, Depends(HooperDependencyClass())]
CommandDependency = Annotated[Command, Depends(CommandDependencyClass())]
ConferenceDependency = Annotated[Conference, Depends(ConferenceDependencyClass())]

ModelHooperDependency = Annotated[models.Hooper, Depends(get_hooper_model)]
ModelCommandDependency = Annotated[models.Command, Depends(get_command_model)]
ModelConferenceDependency = Annotated[models.Conference, Depends(get_conference_model)]
