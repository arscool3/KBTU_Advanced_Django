import requests
from datetime import datetime
from schemas import Bitcoin
from database import session
import numpy as np


def get_latest_date_for_symbol(db: session, symbol: str):
    latest_record = db.query(Bitcoin).filter(Bitcoin.name == symbol).order_by(Bitcoin.end_date.desc()).first()
    return latest_record.end_date if latest_record else None


def get_prices_from_db(db: session, symbol: str, start_date: datetime, end_date: datetime):
    return db.query(Bitcoin.price).filter(
        Bitcoin.name == symbol,
        Bitcoin.start_date >= start_date,
        Bitcoin.end_date <= end_date
    ).all()


def calculate_correlation(prices1, prices2):
    if len(prices1) != len(prices2):
        raise ValueError("Lists of prices must have the same length")

    prices1 = np.array(prices1)
    prices2 = np.array(prices2)

    correlation_matrix = np.corrcoef(prices1, prices2)
    correlation_coefficient = correlation_matrix[0, 1]
    return correlation_coefficient


def fetch_binance_data(symbol, interval, start_str, end_str):
    url = 'https://api.binance.com/api/v3/klines'
    params = {
        'symbol': symbol,
        'interval': interval,
        'startTime': int(datetime.strptime(start_str, '%Y-%m-%d %H:%M:%S').timestamp() * 1000),
        'endTime': int(datetime.strptime(end_str, '%Y-%m-%d %H:%M:%S').timestamp() * 1000),
    }
    response = requests.get(url, params=params)
    data = response.json()

    transformed_data = []
    for candle in data:
        start_timestamp = int(candle[0]) // 1000
        end_timestamp = int(candle[6]) // 1000

        transformed_data.append({
            'name': symbol,
            'price': float(candle[1]),
            'start_date': datetime.fromtimestamp(start_timestamp).strftime('%Y-%m-%d %H:%M:%S'),
            'end_date': datetime.fromtimestamp(end_timestamp).strftime('%Y-%m-%d %H:%M:%S')
        })

    return transformed_data


def insert_data_to_db(name, price, start_date, end_date):
    bitcoin = Bitcoin(name=name, price=price, start_date=start_date, end_date=end_date)
    session.add(bitcoin)
    try:
        session.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()
    finally:
        session.close()