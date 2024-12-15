from datetime import datetime

from pydantic import BaseModel


class CreateCryptoTrade(BaseModel):
    timestamp: datetime = datetime.now()
    currency: str
    k_to_usd: float = 0.0

    class Config:
        from_attributes = True


class CurrencyPair(BaseModel):
    currency: str
    amount: float


class Message(BaseModel):
    start_date: datetime
    end_date: datetime
    sold_currency: CurrencyPair
    purchase_currency: CurrencyPair