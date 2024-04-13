from datetime import datetime

from fastapi import FastAPI

# 127.0.0.1:8002
binance_app = FastAPI(title="BinanceAPI")
import random


def generate_random_currency_value(base_rates):
    fluctuation_percent = 0.05
    random_values = {}
    for currency, base_rate in base_rates.items():
        random_change = base_rate * fluctuation_percent * random.uniform(-1, 1)
        random_values[currency] = round(base_rate + random_change, 5)
    return random_values


def main():
    base_rates = {
        'BTC': 43000,  # Базовый курс для Биткойна к доллару
        'KZT': 0.0023,  # Базовый курс для Тенге к доллару
        'EUR': 1.08,  # Базовый курс для Евро к доллару
        'RUB': 0.012,  # Базовый курс для Рубля к доллару
        'ETH': 3200  # Базовый курс для Эфириума к доллару
    }

    random_currency_values = generate_random_currency_value(base_rates)
    print("Randomized currency values:", random_currency_values)
    return random_currency_values


@binance_app.get("/currencies/", tags=["currency"])
def fake_get():
    data = main()
    now = datetime.now()
    print(now)
    return {"timestamp": now, "data": data}
