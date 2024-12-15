from datetime import datetime

import numpy as np
from fastapi import FastAPI, Depends, WebSocket
from sqlalchemy import select, cast, String
from sqlalchemy.orm import Session

from database import get_db, session
from models import CryptoTrade

app = FastAPI()


@app.websocket("/heatmap")
async def get_heatmap(
        coin1: str,
        coin2: str,
        start_date: datetime = datetime.now(),
):
    coin1_data, coin2_data = get_correlation_matrix(coin1, coin2, start_date)
    return {
        coin1: coin1_data,
        coin2: coin2_data,
    }


def get_correlation_matrix(coin1: str, coin2: str, start_date: datetime):
    coin1_data = get_data_from_db(coin1, start_date)
    coin2_data = get_data_from_db(coin2, start_date)
    return coin1_data, coin2_data,


def get_data_from_db(coin: str, start_date: datetime) -> list[dict]:
    db_session = session()
    trades = db_session.execute(
        select(
            cast(CryptoTrade.timestamp, String).label("timestamp"),
            cast(CryptoTrade.k_to_usd, String).label("k_to_usd")
        ).where(CryptoTrade.currency == coin)
         .where(CryptoTrade.timestamp >= start_date)
    ).all()
    return [{"timestamp": trade.timestamp, "k_to_usd": trade.k_to_usd} for trade in trades]