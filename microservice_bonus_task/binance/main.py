from fastapi import FastAPI
from producer import produce
from schemas import Binance
import uvicorn

app = FastAPI()


@app.get("/")
def hello_world():
    return {"message": "Hello World!"}


@app.post("/binance")
def add_binance(binance: Binance) -> str:
    produce(binance)
    return "Binance has been started producing"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)