from abc import abstractmethod
from pydantic import BaseModel


class BaseSchema(BaseModel):

    class Config:
        from_attributes = True


class AbcRepository:

    @abstractmethod
    def get_all(self):
        raise NotImplementedError()



