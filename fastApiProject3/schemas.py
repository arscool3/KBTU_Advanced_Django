import datetime

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
    created_at: datetime.date

    class Config:
        from_attributes = True


class Country(BaseCountry):
    id: int


class BasePresident(BaseModel):
    name: str
    country: Country

    class Config:
        from_attributes = True


class President(BasePresident):
    id: int
