from fastapi import FastAPI
from database import session
import uvicorn
from consumer import consume

app = FastAPI()


# 8001
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
    return {"message": "Hello World"}


@app.get("/health_check")
def health_check() -> dict:
    return {"message": 'I am alive'}


if __name__ == "__main__":
    consume()
    uvicorn.run(app, host="0.0.0.0", port=8001)
