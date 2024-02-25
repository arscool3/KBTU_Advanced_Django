from abc import abstractmethod
from pydantic import BaseModel
from sqlalchemy.orm import Session
from schemas import ReturnType, Citizen, Country, CreateType
import models as db


class AbcRepository:
    @abstractmethod
    def get_by_id(self, id: int) -> ReturnType:
        raise NotImplementedError()

    @abstractmethod
    def add(self, data: CreateType):
        raise NotImplementedError()


class CitizenRepository(AbcRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> ReturnType:
        db_citizen = self._session.get(db.Citizen, id)
        return Citizen.model_validate(db_citizen)

    def add(self, data: CreateType):
        self._session.add(Citizen(**data.model_dump()))
        self._session.commit()
        self._session.close()
        return "Data added"


