from fastapi import FastAPI
from bot import main
import logging
import sys

app = FastAPI()


@app.on_event("startup")
async def on_start():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await main()


@app.get("/health_check", tags=['check'])
async def health_check() -> dict:
    return {"message": "I'm alive"}
