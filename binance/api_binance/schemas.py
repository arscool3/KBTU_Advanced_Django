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

