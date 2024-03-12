from abc import abstractmethod
from pydantic import BaseModel


class BaseSchema(BaseModel):

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        orm_mode = True


class AbcRepository:

    @abstractmethod
    def get_all(self):
        raise NotImplementedError()



