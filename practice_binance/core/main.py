from fastapi import FastAPI, HTTPException, Depends
from binance.producer import produce
from consumer import healthcheck
from schemas import Binance
from sqlalchemy.orm import Session
from database import session
import models as db

app = FastAPI()

def get_db():
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

@app.get("/data")
async def data(binance_data: Binance):
    produce(binance_data)
    return "Everything is OK!!!"


@app.get("/healthcheck")
async def healthcheck():
    return healthcheck

@app.post("/heatmap")
async def heatmap(coin: str, start_date: str, session: Session = Depends(get_db)):
    c = session.query(db.Data).filter(db.Data.name == coin.name).first()
    return c
