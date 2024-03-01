from abc import abstractmethod

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

import models as db
from schemas import Student


class AbcRepository:
    @abstractmethod
    def __init__(self, session: Session):
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> BaseModel:
        raise NotImplementedError


class StudentRepository(AbcRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> Student:
        db_student = self._session.get(db.Student, id)
        if db_student is None:
            return "No such student!"
        return Student.model_validate(db_student)
