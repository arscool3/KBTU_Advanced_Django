from fastapi import FastAPI
import itertools
import random
from datetime import datetime


app = FastAPI()


# Fake data generation functions
def generate_fake_price():
    return round(random.uniform(1000, 50000), 2)

def generate_fake_volume():
    return round(random.uniform(10, 1000), 2)

def generate_fake_change():
    return round(random.uniform(-5, 5), 2)

def generate_fake_trades():
    return random.randint(100, 10000)



# Endpoints
@app.get("/data/{symbol}")
async def get_ticker(symbol: str):
    return {
        "symbol": symbol,
        "time": str(datetime.now()),
        "price": generate_fake_price(),
        "volume": generate_fake_volume(),
        "change": generate_fake_change(),
        "trades": generate_fake_trades()
    }

