from fastapi import FastAPI
from producer import produce
from schemas import Binance

app = FastAPI()


@app.get("/")
def root():
    return "OK"


@app.post("/binance")
def produce_binance(binance: Binance):
    produce(binance)
    return "Binance works"


# Address: localhost/8000
