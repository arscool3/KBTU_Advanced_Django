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

    class Config:
        from_attributes = True


class Country(BaseCountry):
    id: int
    created_at: date


class CreateCountry(BaseCountry):
    pass


class BasePresident(BaseModel):
    name: str
    country_id: int

    class Config:
        from_attributes = True


class President(BasePresident):
    id: int
    country: Country


class CreatePresident(BasePresident):
    pass
