from datetime import datetime

from pydantic import BaseModel


class Binance(BaseModel):
    symbol: str
    interval: str
    start: str
    end: str


class Price(BaseModel):
    id: int
    time: datetime
    name: str
    price: float

    class Config:
        orm_mode = True