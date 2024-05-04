# from core.producer import produce
import asyncio
import time
from datetime import datetime
import random
from fastapi import FastAPI, Depends, HTTPException, WebSocket, Response

app = FastAPI()

trade_pairs = [
    'BTC-USD', 'USD-BTC', 'ETH-USD', 'ETH-BTC', 'LTC-USD', 'LTC-BTC',
]

@app.websocket('/data')
async def generate_trade(web_socket: WebSocket):
    await web_socket.accept()

    try:
        while True:
            price = random.randint(69000, 72000)
            trade_unit = random.choice(trade_pairs)
            quantity=random.randint(1, 100)
            await web_socket.send_json({'pair': trade_unit, 'price': price, 'quantity': quantity})
            await asyncio.sleep(2)
    except Exception as e:
        print(e)
    finally:
        await web_socket.close()

