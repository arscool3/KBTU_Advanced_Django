from abc import abstractmethod
from pydantic import BaseModel
from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from database import Base


class AbcRepository:
    model: Base = None
    action_schema: dict[str, BaseModel] = {}
    session: Session = None

    @abstractmethod
    def get_by_id(self, id: int):
        raise NotImplementedError()

    @abstractmethod
    def list(self):
        raise NotImplementedError()

    @abstractmethod
    def create(self, body: BaseModel):
        raise NotImplementedError()

    @abstractmethod
    def delete(self, id: int):
        raise NotImplementedError()

    def get_schema(self, keyword: str):
        schema = self.action_schema.get(keyword)
        if not schema:
            raise KeyError(f"No schema assigned for action {keyword}")
        return schema


class BaseRepository(AbcRepository):

    def get_by_id(self, id: int):
        instance = self.session.get(self.model, id)
        schema: BaseModel = self.get_schema("get_by_id")
        return schema.model_validate(instance)

    def list(self):
        instances = self.session.execute(select(self.model)).scalars().all()
        schema: BaseModel = self.get_schema("list")
        return [schema.model_validate(instance) for instance in instances]

    def create(self, body: BaseModel):
        self.session.add(self.model(**body.model_dump()))
        self.session.commit()
        return body

    def delete(self, id: int):
        self.session.execute(delete(self.model).where(self.model.id == id))
        self.session.commit()
        return "Deleted"
