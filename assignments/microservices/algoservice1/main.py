from fastapi import FastAPI
from database import session

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
