from fastapi import FastAPI
from producer import produce
from consumer import healthcheck

app = FastAPI()


@app.get("/data")
async def data(symbol: str, interval: str, start: str, end: str):
    val = {
        "symbol": symbol,
        "interval": interval,
        "start": start,
        "end": end,
    }
    produce(val)


@app.get("/healthcheck")
async def healthcheck():
    return healthcheck
