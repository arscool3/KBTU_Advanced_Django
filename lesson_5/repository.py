from abc import abstractmethod
from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from schemas import Citizen, Country, President
import models


class AbcRepository:

    @abstractmethod
    def get_by_id(self, id: int) -> Citizen | Country | President:
        raise NotImplementedError()

    def get_all(self) -> List[Citizen] | List[Country] | List[President]:
        raise NotImplementedError()


class CitizenRepository(AbcRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> Citizen:
        db_citizen = self._session.get(models.Citizen, id)
        return Citizen.model_validate(db_citizen)

    def get_all(self) -> List[Citizen]:
        db_citizens = self._session.execute(select(models.Citizen)).scalars().all()
        return [Citizen.model_validate(db_citizen) for db_citizen in db_citizens]


class CountryRepository(AbcRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> Country:
        db_country = self._session.get(models.Country, id)
        print(f"{db_country=}")
        return Country.model_validate(db_country)

    def get_all(self) -> List[Country]:
        db_countries = self._session.execute(select(models.Country)).scalars().all()
        return [Country.model_validate(db_country) for db_country in db_countries]


class PresidentRepository(AbcRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> President:
        db_president = self._session.get(models.President, id)
        return President.model_validate(db_president)

    def get_all(self) -> List[President]:
        db_presidents = self._session.execute(select(models.President)).scalars().all()
        return [President.model_validate(db_president) for db_president in db_presidents]
