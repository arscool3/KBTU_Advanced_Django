from fastapi import FastAPI
from urls import router

app = FastAPI()

app.include_router(router)


@app.get("/health_check/")
def health_check():
    return {"message": "OK"}
