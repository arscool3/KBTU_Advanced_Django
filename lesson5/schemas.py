from datetime import date
from pydantic import BaseModel


class BaseCitizen(BaseModel):
    name: str
    age: int

    class Config:
        from_attributes = True


class Citizen(BaseCitizen):
    id: int


class CreateCitizen(BaseCitizen):
    pass


class Country(BaseModel):
    id: int
    name: str
    created_at: date

    class Config:
        from_attributes = True


class President(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


ReturnType = Citizen | Country | President
CreateType = CreateCitizen
