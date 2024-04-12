from datetime import datetime

from pydantic import BaseModel


class CreateData(BaseModel):
    time: datetime
    name: str
    k_to_usd: float = 0.0


class Currency(BaseModel):
    cur_name: str
    k: str
    amount: float


class CurrencyPair(BaseModel):
    send_coin: Currency
    get_coin: Currency


class Binance(BaseModel):
    start_date: str
    end_date: str
    interval: str
    pair: CurrencyPair

