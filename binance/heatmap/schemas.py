from datetime import datetime

from pydantic import BaseModel


class Currency(BaseModel):
    cur_name: str
    k: str


class CurrencyPair(BaseModel):
    send_coin: Currency
    get_coin: Currency


class Binance(BaseModel):
    start_date: str
    end_date: str
    interval: str
    pair: CurrencyPair


class DataSchema(BaseModel):
    id: int
    time: datetime
    name: str
    k_to_usd: float

    class Config:
        from_attributes = True


class CreateData(BaseModel):
    time: datetime
    name: str
    k_to_usd: float = 0.0
