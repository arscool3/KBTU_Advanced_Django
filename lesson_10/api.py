import asyncio
import random

from fastapi import FastAPI, WebSocket

app = FastAPI()

stock_units = [
    'AAPL', 'KSPI', 'TSLA', 'SAMSUNG', 'NVIDIA', 'SpaceX', 'JNJ',
]


@app.websocket('/data')
async def stock_market(web_socket: WebSocket):
    await web_socket.accept()
    try:
        while True:
            price = random.randint(660, 670)
            if price == 666:
                raise Exception('devil here')
            stock_unit = random.choice(stock_units)
            await web_socket.send_json({'stock': stock_unit, 'price': price})
            await asyncio.sleep(2)
    except Exception as e:
        print(f"Error {e}")
    finally:
        await web_socket.close()
