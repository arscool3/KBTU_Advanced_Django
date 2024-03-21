from abc import ABC, abstractmethod

from pydantic import BaseModel
from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from database import Base


class AbcRepository(ABC):
    model: Base = None
    session: Session = None
    schema: BaseModel = None

    @abstractmethod
    def get_list(self):
        raise NotImplementedError()

    @abstractmethod
    def create(self, body: BaseModel):
        raise NotImplementedError()

    @abstractmethod
    def retrieve(self, id: int):
        raise NotImplementedError()

    @abstractmethod
    def delete(self, id: int):
        raise NotImplementedError()


class BaseRepository(AbcRepository):

    def get_list(self):
        instances = self.session.execute(select(self.model)).scalars().all()
        return [self.schema.model_validate(instance) for instance in instances]

    def create(self, body: BaseModel):
        instance = self.model(**body.model_dump())
        self.session.add(instance)
        return "Your instance is created"

    def retrieve(self, id: int):
        instance = self.session.get(self.model, id)
        return self.schema.model_validate(instance)

    def delete(self, id: int):
        self.session.execute(delete(self.model).where(self.model.id == id))
        return "Your instance is deleted"
