from pydantic import BaseModel


class OwnerBase(BaseModel):
    name: str


class CarBase(BaseModel):
    vin: str
    plate: str
    model: str
    year: int


class Owner(OwnerBase):
    id: int

    class Config:
        orm_mode = True


class Car(CarBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class OwnerCreate(OwnerBase):
    pass


class CarCreate(CarBase):
    owner_id: int
