from fastapi import FastAPI
from datetime import datetime

# 127.0.0.1:8003
producer_server = FastAPI(title="ProducerServer")

@producer_server.get("/healthcheck/", tags=["healthcheck"])
def fake_get():
    return {"healthcheck": "ok", "timestamp": datetime.now()}

