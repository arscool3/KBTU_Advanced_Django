from abc import ABC, abstractmethod

from pydantic import BaseModel
from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from app.database import Base


class AbcRepository(ABC):
    model: Base = None
    action_schema: dict[str, BaseModel] = {}
    session: Session = None

    @abstractmethod
    def list(self):
        raise NotImplementedError()

    @abstractmethod
    def retrieve(self, id: int):
        raise NotImplementedError()

    @abstractmethod
    def create(self, body: BaseModel):
        raise NotImplementedError()

    @abstractmethod
    def delete(self, id: int):
        raise NotImplementedError()

    def get_schema(self, action_key: str):
        schema = self.action_schema.get(action_key)
        if not schema:
            raise KeyError(f"No schema assigned for action {action_key}")
        return schema


class BaseRepository(AbcRepository):

    def list(self):
        instances = self.session.execute(select(self.model)).scalars().all()
        schema: BaseModel = self.get_schema("list")
        return [schema.model_validate(instance) for instance in instances]

    def retrieve(self, id: int):
        instance = self.session.get(self.model, id)
        schema: BaseModel = self.get_schema("retrieve")
        return schema.model_validate(instance)

    def create(self, body: BaseModel):
        instance = self.model(**body.model_dump())
        self.session.add(instance)
        self.session.commit()

        schema: BaseModel = self.get_schema("create")
        return schema.model_validate(instance)

    def delete(self, id: int):
        self.session.execute(delete(self.model).where(self.model.id == id))
        self.session.commit()
        return """Deleted successfully"""