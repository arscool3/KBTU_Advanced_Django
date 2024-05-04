import asyncio
import random
from datetime import datetime

from fastapi import FastAPI, WebSocket
from pydantic import BaseModel

app = FastAPI()


@app.websocket("/binance")
async def binance_data(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await websocket.send_json(_get_mock_data())
            await asyncio.sleep(2)
    except Exception as e:
        print(e)
    finally:
        await websocket.close()


class Trade(BaseModel):
    currency: str
    amount: float


def _get_mock_data() -> dict:
    currency_choices = ["btc", "etherium"]

    index = random.randint(0, 1)

    data = {
        "start_date": datetime.now(),
        "end_date": datetime.now(),
        "sold_currency": Trade(currency=currency_choices[index], amount=1).model_dump(),
        "purchase_currency": Trade(currency=currency_choices[(index + 1) // 2], amount=70000).model_dump(),
    }

    return data