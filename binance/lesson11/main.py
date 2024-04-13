from fastapi import FastAPI
from database import session
from consumer import consume

app = FastAPI()


@app.get("/")
def root():
    return "OK"


@app.get("/heath_check")
def health_check() -> str:
    return "I'm alive"


if __name__ == "__main__":
    consume()


# Address: localhost/8002
