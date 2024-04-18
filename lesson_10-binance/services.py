import requests
from datetime import datetime
from schemas import Bitcoin
from db import session

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
