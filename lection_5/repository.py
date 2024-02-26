from abc import abstractmethod

import models as m
from schemas import *
from sqlalchemy.orm import Session


class AbcRepository:
    def __init__(self, db: Session):
        self._session = db
        self.return_model = None

    @abstractmethod
    def get_by_id(self, id: int) -> Citizen | President | Country:
        raise NotImplementedError()


class CitizenRepository(AbcRepository):
    def get_by_id(self, id: int) -> Citizen:
        db_citizen = self._session.get(m.Citizen, id)

        citizen = Citizen.model_validate(db_citizen)
        return citizen


class CountryRepository(AbcRepository):
    def get_by_id(self, id: int) -> Country:
        db_country = self._session.get(m.Country, id)

        country = Country.model_validate(db_country)
        return country


class PresidentRepository(AbcRepository):
    def get_by_id(self, id: int) -> President:
        db_president = self._session.get(m.President, id)

        president = President.model_validate(db_president)
        return president
