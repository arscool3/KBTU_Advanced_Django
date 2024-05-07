import random
import time

from fastapi import FastAPI

app = FastAPI()


def test(name: str):
    return not name == "Arslan"


@app.get("/drug")
def drug_endpoint(name: str):
    time.sleep(10)
    return test(name)


@app.get("/psycho")
def psycho_endpoint(name: str):
    time.sleep(15)
    return test(name)


@app.get("/crime")
def crime_endpoint(name: str):
    time.sleep(10)
    return test(name)