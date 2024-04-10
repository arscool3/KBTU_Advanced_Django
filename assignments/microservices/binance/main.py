from fastapi import FastAPI
from producer import produce
from schemas import Binance

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/binance")
def produce_binance(binance: Binance) -> str:
    produce(binance)
    return "Binance has been produces"
