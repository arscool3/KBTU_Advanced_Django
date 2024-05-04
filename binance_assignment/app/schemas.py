from datetime import datetime

from pydantic import BaseModel


class CurrencyPair(BaseModel):
    first_currency: str
    second_currency: str


class BinanceDeal(BaseModel):
    pair: str
    price: float
    quantity: int
