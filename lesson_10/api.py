import asyncio
import json

from fastapi import FastAPI, WebSocket
from services import fetch_binance_data

app = FastAPI()

symbols = ['BTCUSDT', 'ETHUSDT']
interval = '1h'
start_date = '2022-01-01 00:00:00'
end_date = '2022-01-02 00:00:00'


@app.websocket('/data')
async def stock_market(web_socket: WebSocket):
    await web_socket.accept()
    try:
        while True:
            for symbol in symbols:
                data = fetch_binance_data(symbol, interval, start_date, end_date)
                for entry in data:
                    await web_socket.send_json(json.dumps(entry))
                    await asyncio.sleep(2)
    except Exception as e:
        print(f"Error {e}")
    finally:
        await web_socket.close()