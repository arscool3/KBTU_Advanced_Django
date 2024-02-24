from abc import abstractmethod

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

import models as db
from schemas import Citizen, Country


class AbcRepository:

    @abstractmethod
    def get_by_id(self, id: int) -> BaseModel:
        raise NotImplementedError()


class CitizenRepository(AbcRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> Citizen:
        db_citizen = self._session.get(db.Citizen, id).first()
        return Citizen.model_validate(db_citizen)


class CountryRepository(AbcRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id: int) -> Country:
        pass