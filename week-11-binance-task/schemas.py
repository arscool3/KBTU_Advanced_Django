from pydantic import BaseModel
from datetime import datetime


class BaseBitcoin(BaseModel):
    time: datetime
    price: float
    coin: str

    class Config:
        from_attributes = True


class Bitcoin(BaseBitcoin):
    id: int

class BitcoinCreate(BaseBitcoin):
    pass

