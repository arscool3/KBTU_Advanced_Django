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
    age: int

    class Config:
        from_attributes = True


class Country(BaseCitizen):
    id: int


class CreateCountry(BaseCitizen):
    pass


class BasePresident(BaseModel):
    name: str
    age: int

    class Config:
        from_attributes = True


class President(BaseCitizen):
    id: int


class CreatePresident(BaseCitizen):
    pass
