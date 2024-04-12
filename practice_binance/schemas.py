from pydantic import BaseModel
from datetime import datetime


class Price(BaseModel):
    id: int
    time: datetime
    name: str
    price: float

    class Config:
        orm_mode = True