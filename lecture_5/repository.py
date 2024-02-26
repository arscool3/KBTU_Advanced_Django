from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

import models as md
import schemas as sc


class AbcRepository:

    def get_by_id(self, id: int) -> BaseModel:
        raise NotImplementedError()


class CitizenRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> sc.Citizen:
        db_citizen = self._session.get(md.Citizen, id)
        return sc.Citizen.model_validate(db_citizen)


class CountryRepository(AbcRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id: int) -> sc.Country:
        db_country = self._session.get(md.Country, id)
        return sc.Country.model_validate(db_country)


class PresidentRepository(AbcRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id: int) -> sc.Country:
        db_president = self._session.get(md.President, id)
        return sc.Country.model_validate(db_president)
