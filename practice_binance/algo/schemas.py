from datetime import datetime

from pydantic import BaseModel


class Data(BaseModel):
    time: datetime
    name: str
    price: float


class Price(BaseModel):
    id: int
    time: datetime
    name: str
    price: float

    class Config:
        orm_mode = True