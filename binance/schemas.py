from datetime import datetime
from pydantic import BaseModel

class BaseCurrency(BaseModel):
    time: datetime
    price: float
    coin: str

    class Config:
        from_attributes = True


class Currency(BaseCurrency):
    id: int

class CurrencyCreate(BaseCurrency):
    pass