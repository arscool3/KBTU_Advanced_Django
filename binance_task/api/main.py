from datetime import datetime

import numpy as np
from fastapi import FastAPI, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db, session
from models import CryptoTrade

app = FastAPI()


@app.get("/heatmap")
async def get_heatmap(
        coin1: str,
        coin2: str,
        start_date: datetime = datetime.now(),
):
    data1 = get_data_from_db(coin1, start_date)
    data2 = get_data_from_db(coin2, start_date)
    correlation_matrix = np.corrcoef(data1, data2)

    print(correlation_matrix)

    return correlation_matrix


def get_data_from_db(coin: str, start_date: datetime) -> list[float]:
    db_session = session()
    trades = (db_session
              .execute(select(CryptoTrade.k_to_usd)
                       .where(CryptoTrade.sold_currency == coin)
                       .where(CryptoTrade.timestamp >= start_date))
              .scalars().all()
              )
    return trades
