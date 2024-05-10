from fastapi import FastAPI
from producer import produce
from schemas import Binance
import uvicorn

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


# 8000
@app.post("/binance")
def produce_binance(binance: Binance) -> str:
    produce(binance)
    return "Binance has been produces"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
