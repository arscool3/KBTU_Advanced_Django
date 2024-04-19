from pydantic import BaseModel


class BaseBitcoin(BaseModel):
    name: str
    price: float
    start_date: str
    end_date: str

    class Config:
        from_attributes = True


class Bitcoin(BaseBitcoin):
    id: int


class BitcoinCreate(BaseBitcoin):
    pass