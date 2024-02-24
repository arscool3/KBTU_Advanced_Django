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


class CreateCountry(BaseCountry):
    pass


class Country(BaseCountry):
    id: int


class BasePresident(BaseModel):
    name: str
    country: Country

    class Config:
        from_attributes = True


class CreatePresident(BasePresident):
    country_id: int

class PresidentCountry(BasePresident):
    name: str

class President(BasePresident):
    id: int
    country = PresidentCountry
