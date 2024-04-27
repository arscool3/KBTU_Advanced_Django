from datetime import datetime

from pydantic import BaseModel


class CurrencyQueryRequest(BaseModel):
    name: str
    start_date: datetime
    end_date: datetime


class CurrencyData(BaseModel):
    name: str
    timestamp: datetime
    coefficient: float

    class Config:
        from_attributes = True