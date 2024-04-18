import requests
from datetime import datetime
from schemas import Bitcoin
from db import session


# def fetch_binance_data(symbol, interval, start_str, end_str):
#     url = 'https://api.binance.com/api/v3/klines'
#     params = {
#         'symbol': symbol,
#         'interval': interval,
#         'startTime': int(datetime.strptime(start_str, '%Y-%m-%d %H:%M:%S').timestamp() * 1000),
#         'endTime': int(datetime.strptime(end_str, '%Y-%m-%d %H:%M:%S').timestamp() * 1000),
#     }
#     response = requests.get(url, params=params)
#     data = response.json()
#
#     return [
#         {
#             'name': symbol,
#             'price': candle[1],
#             'start_date': datetime.fromtimestamp(candle[0] / 1000).strftime('%Y-%m-%d %H:%M:%S'),
#             'end_date': datetime.fromtimestamp(candle[9] / 1000).strftime('%Y-%m-%d %H:%M:%S')
#         } for candle in data
#     ]
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
        # Convert the timestamp and closing time to integer before performing the division
        start_timestamp = int(candle[0]) // 1000  # Opening time is the first element
        end_timestamp = int(candle[6]) // 1000  # Closing time is the seventh element

        transformed_data.append({
            'name': symbol,
            'price': float(candle[1]),  # Open price is the second element, convert string to float
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
