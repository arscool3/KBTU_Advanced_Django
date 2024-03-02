from datetime import date

from pydantic import BaseModel


class BaseCountry(BaseModel):
    name: str

    class Config:
        from_attributes = True


class Country(BaseCountry):
    id: int
    created_at: date


class BaseCitizen(BaseModel):
    name: str
    age: int
    country_id: int

    class Config:
        from_attributes = True


class Citizen(BaseCitizen):
    id: int
    country: Country


class CountryWithCitizens(Country):
    citizens: list[BaseCitizen]


class CreateCitizen(BaseCitizen):
    pass


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


class CountryWithPresident(Country):
    president: President


class BaseUnion(BaseModel):
    name: str

    class Config:
        from_attributes = True


class Union(BaseUnion):
    id: int


class UnionWithCountries(BaseUnion):
    countries: list[Country]
