import asyncio
import random
from datetime import timedelta, datetime

from fastapi import FastAPI, WebSocket


app = FastAPI()


def random_date(start, end):
    delta = end - start
    random_days = random.randrange(delta.days)
    return start + timedelta(days=random_days)


@app.websocket("/data")
async def stock_market(web_socket: WebSocket):
    await web_socket.accept()
    start_period = datetime.strptime("20210101", "%Y%m%d")
    end_period = datetime.strptime("20211231", "%Y%m%d")
    try:
        while True:
            start_date = random_date(start_period, end_period)
            end_date = random_date(start_date, end_period)

            purchase_price = round(random.uniform(30000, 40000), 2),
            sell_price = round(random.uniform(30000, 40000), 2),
            start_date = start_date.strftime("%Y%m%d"),
            end_date = end_date.strftime("%Y%m%d")
            await web_socket.send_json("purchase_price": purchase_price, "sell_price": sell_price, "start_date": start_date, "end_date": end_date)
            await asyncio.sleep(5)
    except Exception as e:
        print(f"Error {e}")
    finally:
        await web_socket.close()



