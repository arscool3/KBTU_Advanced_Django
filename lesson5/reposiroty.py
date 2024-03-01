from abc import abstractmethod
from pydantic import BaseModel
from sqlalchemy.orm import Session
from schemas import ReturnType, Citizen, Country, CreateType, President
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
        return "Citizen added"


class CountryRepository(AbcRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> ReturnType:
        db_country = self._session.get(db.Country, id)
        return Country.model_validate(db_country)

    def add(self, data: CreateType):
        self._session.add(Country(**data.model_dump()))
        self._session.commit()
        self._session.close()
        return "Country added"


class PresidentRepository(AbcRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> ReturnType:
        db_president = self._session.get(db.President, id)
        return President.model_validate(db_president)

    def add(self, data: CreateType):
        self._session.add(President(**data.model_dump()))
        self._session.commit()
        self._session.close()
        return "Country added"


