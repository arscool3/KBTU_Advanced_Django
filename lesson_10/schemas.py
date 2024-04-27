from pydantic import BaseModel
from database import Base


class BaseBitcoin(BaseModel):
    name: str
    price: float
    start_date: str
    end_date: str

    class Config:
        from_attributes = True


class Bitcoin(BaseBitcoin):
    id: int