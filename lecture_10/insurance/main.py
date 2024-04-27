from fastapi import FastAPI

# 127.0.0.1:8003
binance_app = FastAPI(title="ProducerServer")



@binance_app.get("/healthcheck/", tags=["healthcheck"])
def fake_get():
    return {"healthcheck": "ok"}
