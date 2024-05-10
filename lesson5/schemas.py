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


class BaseCountry(BaseModel):
    name: str
    created_at: date

    class Config:
        from_attributes = True


class Country(BaseModel):
    id: int


class CreateCountry(BaseCountry):
    pass


class BasePresident(BaseModel):
    name: str

    class Config:
        from_attributes = True


class President(BaseModel):
    id: int


class CreatePresident(BasePresident):
    pass

ReturnType = Citizen | Country | President
CreateType = CreateCitizen | CreateCountry | CreatePresident


