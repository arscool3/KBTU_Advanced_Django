from pydantic import BaseModel


class Coin(BaseModel):
    code: str
    coefficient: str


class Pair(BaseModel):
    from_coin: Coin
    at_coin: Coin


class Binance(BaseModel):
    interval: str
    start_date: str
    end_date: str
    pair: Pair
