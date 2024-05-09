from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import FileResponse
from consumer import consume
from producer import produce
from database import session, Currency

from datetime import datetime
from pydantic import BaseModel

class BaseCurrency(BaseModel):
    time: datetime
    price: float
    coin: str

    class Config:
        from_attributes = True


class Currency(BaseCurrency):
    id: int

class CurrencyCreate(BaseCurrency):
    pass

app = FastAPI()

def create_growth_graph(currency):
    times = [entry.time for entry in currency]
    prices = [entry.price for entry in currency]

    return [(times[i], prices[i]) for i in range(len(times))]

@app.get("/currency/run")
def run_server(background_tasks: BackgroundTasks):
    background_tasks.add_task(produce)
    background_tasks.add_task(consume)
    return "Producer and consumer started"

@app.get("/currency/{currency_name}")
async def get_currency_prices(coin_name: str):
    currency = session.query(Currency).filter_by(coin=coin_name).all()
    print(f'{coin_name} has {len(currency)} entry')
    session.close()
    return create_growth_graph(currency)
