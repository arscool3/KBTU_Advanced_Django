from fastapi import FastAPI, BackgroundTasks
from producer import produce
from schemas import Binance

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


# 8000
@app.post("/binance")
def produce_binance(binance: Binance) -> str:
    background_tasks = BackgroundTasks()
    background_tasks.add_task(produce, binance)
    return "Binance has been produces"
