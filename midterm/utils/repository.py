from abc import ABC, abstractmethod

from pydantic import BaseModel
from sqlalchemy.orm import Session


class AbcRepository(ABC):
    session: Session = None
    @abstractmethod
    def list(self):
        raise NotImplementedError

    @abstractmethod
    def retrieve(self, id: int):
        raise NotImplementedError

    @abstractmethod
    def create(self, body: BaseModel) -> str:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: int):
        raise NotImplementedError
