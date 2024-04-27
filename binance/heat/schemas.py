from pydantic import BaseModel
from datetime import datetime

class BitcoinExchangeRateSchema(BaseModel):
    start_time: datetime
    end_time: datetime
    name: str
    k_to_usd: float