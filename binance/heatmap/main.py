from typing import Optional

from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.testing import db

from database import session
from schemas import DataSchema

app = FastAPI()


def get_db():
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


@app.get("/")
def root():
    return "OK"


class HeatmapResponse(BaseModel):
    coin1: Optional[DataSchema]
    coin2: Optional[DataSchema]


@app.get("/get_heatmap", response_model=HeatmapResponse)
def get_heatmap(coin1: DataSchema, coin2: DataSchema, session: Session = Depends(get_db)):
    coin1_data = session.query(db.Data).filter(db.Data.name == coin1.name).first()
    coin2_data = session.query(db.Data).filter(db.Data.name == coin2.name).first()
    return {"coin1": coin1_data, "coin2": coin2_data}

# Address: localhost/8001
