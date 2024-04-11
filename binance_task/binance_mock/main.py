from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/binance")
async def binance_data():
    return _get_mock_data()


class Trade(BaseModel):
    currency: str
    amount: float


def _get_mock_data() -> dict:
    data = {
        "start_date": datetime.now(),
        "end_date": datetime.now(),
        "sold_currency": Trade(currency="etherium", amount=1).model_dump(),
        "purchase_currency": Trade(currency="usdt", amount=70000).model_dump(),
    }

    return data
