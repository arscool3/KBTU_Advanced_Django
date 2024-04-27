import asyncio
import json
from datetime import datetime

import confluent_kafka
import websockets

from database import Data
from database import get_db
from schemas import CreateData, Binance

consumer = confluent_kafka.Consumer(
    {"bootstrap.servers": "localhost:9092", "group.id": "main_group"}
)
topic = "main_topic"
consumer.subscribe([topic])
number_of_messages = 10


def health_check():
    return "I'm alive"


async def consume(websocket):
    try:
        while True:
            message = await websocket.recv()
            binance = Binance.model_validate(json.loads(message))
            send_coin_amount = binance.pair.send_coin.amount
            get_coin_amount = binance.pair.get_coin.amount

            if send_coin_amount is not None and get_coin_amount is not None and get_coin_amount != 0:
                k_to_usd = send_coin_amount - get_coin_amount / get_coin_amount
            else:
                k_to_usd = 0.0

            db = next(get_db())
            tradeData = CreateData(
                time=datetime.now(),
                name=f'{binance.pair.send_coin.cur_name}_to_{binance.pair.get_coin.cur_name}',
                k_to_usd=k_to_usd
            )
            db.add(Data(**tradeData.model_dump()))
            print("Data has been inserted")
            db.commit()
    except Exception as e:
        print(f"Raised {e}")
    finally:
        db.close()


async def start_consumer():
    url = "ws://localhost:8765"
    async with websockets.connect(url) as websocket:
        await consume(websocket)


if __name__ == '__main__':
    asyncio.run(start_consumer())
    # try:
    #     consume()
    # finally:
    #     consumer.close()
