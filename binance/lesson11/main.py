from fastapi import FastAPI
from database import session
from lesson11.core.consumer import consume

app = FastAPI()


def get_db():
    try:
        yield session
        session.commit()
    except Exception:
        raise
    finally:
        session.close()


@app.get("/")
def root():
    return "OK"


@app.get("/heath_check")
def health_check() -> str:
    return "I'm alive"


if __name__ == "__main__":
    consume()

# Address: localhost/8002
