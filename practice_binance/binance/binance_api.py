import requests
import pandas as pd
from datetime import datetime
import json


def fetch_binance_price_history(symbol, interval, start_str, end_str=None):
    start_time = int(datetime.strptime(start_str, "%Y-%m-%d").timestamp() * 1000)
    end_time = int(datetime.strptime(end_str, "%Y-%m-%d").timestamp() * 1000) if end_str else None

    url = 'https://api.binance.com/api/v3/klines'
    params = {
        'symbol': symbol,
        'interval': interval,
        'startTime': start_time,
        'endTime': end_time,
        'limit': 1000
    }

    response = requests.get(url, params=params)
    data = response.json()

    df = pd.DataFrame(data, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time',
                                     'Quote asset volume', 'Number of trades', 'Taker buy base asset volume',
                                     'Taker buy quote asset volume', 'Ignore'])

    df['Open time'] = pd.to_datetime(df['Open time'], unit='ms')
    df['Close time'] = pd.to_datetime(df['Close time'], unit='ms')

    df = df[['Open time', 'Open', 'High', 'Low', 'Close', 'Volume']]

    json_data = df.to_json(orient='records', date_format='iso')
    return json_data




# Example usage
# symbol = 'BTCUSDT'
# interval = '1h'  # 1 hour interval
# start_str = '2023-01-9'
# end_str = '2024-01-10'
#
# # Fetch the price history
# price_history = fetch_binance_price_history(symbol, interval, start_str, end_str)
# formatted_json = json.dumps(json.loads(price_history), indent=4)
# print(formatted_json)


