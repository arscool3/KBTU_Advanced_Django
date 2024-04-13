from pydantic import BaseModel
from datetime import datetime


class Bitcoin(BaseModel):
    time: datetime
    price: float
    coin: str

