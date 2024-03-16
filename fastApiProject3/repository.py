from abc import abstractmethod

from sqlalchemy.orm import Session

from schemas import Citizen, President, Country
import models


class AbcRepository:

    @abstractmethod
    def get_by_id(self, id: int) -> Citizen | Country | President:
        raise NotImplementedError()


class CitizenRepository(AbcRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id: int) -> Citizen:
        citizen = self.session.get(models.Citizen, id)
        return Citizen.model_validate(citizen)


class CountryRepository(AbcRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id: int) -> Country:
        country = self.session.get(models.Country, id)
        return Country.model_validate(country)


class PresidentRepository(AbcRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id: int) -> President:
        president = self.session.get(models.President, id)
        return President.model_validate(president)
