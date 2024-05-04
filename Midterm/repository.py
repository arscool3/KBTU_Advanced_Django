from abc import abstractmethod
from pydantic import BaseModel
from sqlalchemy.orm import Session


class AbcRepository:

    def __init__(self, session: Session):
        self.session = session

    @abstractmethod
    def get_by_id(self, id: int):
        raise NotImplementedError()

    @abstractmethod
    def get_all(self):
        raise NotImplementedError()

    @abstractmethod
    def create(self, body: BaseModel):
        raise NotImplementedError()

    @abstractmethod
    def delete(self, id: int):
        raise NotImplementedError()
