import itertools
import random
from datetime import datetime

from fastapi import FastAPI

# 127.0.0.1:8543
binance_app = FastAPI(title="BinanceFastAPI")

currencies = ["usd", "btc", "eur", "gbp", "eth", "kzt"]

currencies = [a[0] + a[1] for a in itertools.combinations(currencies, 2)]


@binance_app.get("/fake/binance/data/", tags=["fake"])
def fake_get():
    fake_data = {}

    for currency in currencies:
        fake_data[currency] = round(random.uniform(0, 100), 5)

    now = datetime.now()

    return {"timestamp": now, "data": fake_data}
