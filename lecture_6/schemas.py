from pydantic import BaseModel


class BaseHuman(BaseModel):
    name: str
    age: int

    class Config:
        from_attributes = True


class Human(BaseHuman):
    id: int


class CreateHuman(BaseHuman):
    pass


class BaseDog(BaseModel):
    name: str
    age: int

    class Config:
        from_attributes = True


class Dog(BaseDog):
    id: int


class CreateDog(BaseDog):
    pass


class BaseCat(BaseModel):
    name: str
    age: int

    class Config:
        from_attributes = True


class Cat(BaseCat):
    id: int


class CreateCat(BaseCat):
    pass


class BaseHouse(BaseModel):
    name: str
    age: int

    class Config:
        from_attributes = True


class House(BaseHouse):
    id: int


class CreateHouse(BaseHouse):
    pass
