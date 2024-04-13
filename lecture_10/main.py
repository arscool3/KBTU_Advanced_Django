from http.client import HTTPException
from typing import List

from fastapi import FastAPI, Depends
from datetime import datetime

from sqlalchemy.orm import Session

import database as models
from schemas import CurrencyQueryRequest, CurrencyData

# 127.0.0.1:8000
heat_map = FastAPI(title="HeatMapAPI")


def get_db():
    try:
        db = Session(models.engine)
        yield db
        db.commit()
    except:
        raise
    finally:
        db.close()


@heat_map.get("/healthcheck/", tags=["healthcheck"])
def fake_get():
    return {"healthcheck": "ok", "timestamp": datetime.now()}


@heat_map.post("/currency_query/", response_model=List[CurrencyData])
def post_currency_query(
        query_params: CurrencyQueryRequest,
        db: Session = Depends(get_db)
):
    currency_data = (
        db.query(models.Currency)
        .filter(models.Currency.name == query_params.name)
        .filter(models.Currency.timestamp >= query_params.start_date)
        .filter(models.Currency.timestamp <= query_params.end_date)
        .all()
    )
    print(query_params.name, query_params.start_date, query_params.end_date)
    if not currency_data:
        print("No currencies found")

    return currency_data
