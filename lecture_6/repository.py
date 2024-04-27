from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

import models as md
import schemas as sc


class AbcRepository:

    def get_by_id(self, id: int) -> BaseModel:
        raise NotImplementedError()


class HumanRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> sc.Human:
        db_human = self._session.get(md.Human, id)
        return sc.Human.model_validate(db_human)


class CatRepository(AbcRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> sc.Cat:
        db_cat = self._session.get(md.Cat, id)
        return sc.Cat.model_validate(db_cat)


class DogRepository(AbcRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> sc.Dog:
        db_dog = self._session.get(md.Dog, id)
        return sc.Dog.model_validate(db_dog)

class HouseRepository(AbcRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> sc.House:
        db_house = self._session.get(md.House, id)
        return sc.House.model_validate(db_house)
