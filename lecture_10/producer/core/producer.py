import os
import pickle
import time
# from dotenv import load_dotenv
import confluent_kafka
import httpx
import asyncio
import json
from datetime import datetime

import websockets
from websockets import ConnectionClosedOK

# dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

# if os.path.exists(dotenv_path):
#     load_dotenv(dotenv_path)
# else:
#     print("Error: .env file")

KAFKA_BOOTSTRAP = os.environ.get("KAFKA_BOOTSTRAP", "localhost: 9092")
binance_host = os.environ.get("INTERNAL_BINACE_HOST", "127.0.0.1:8002")
topic = os.environ.get("DEFAULT_TOPIC", "main_topic")

producer = confluent_kafka.Producer({"bootstrap.servers": KAFKA_BOOTSTRAP})


def request_binance():
    time.sleep(2)  # to not DOS a server
    url = f"http://{binance_host}/currencies/"
    response = httpx.get(url)
    print(response.json())
    return response.json()


def produce(res: dict) -> None:
    to_send = pickle.dumps(res)
    producer.produce(topic=topic, value=to_send)
    producer.flush()


async def test_ws():
    url = f'ws://{binance_host}/currencies/'
    try:
        async with websockets.connect(url) as websocket:
            while True:
                data = await websocket.recv()
                data = json.loads(data)
                data['timestamp'] = datetime.strptime(data['timestamp'], "%Y-%m-%d %H:%M:%S")
                produce(data)
                print(data)
    except ConnectionClosedOK as e:
        print('Connection was closed')

asyncio.run(test_ws())
# if __name__ == "__main__":
#     while True:
#         # res = request_binance()
#         # produce(res)
#         try:
#             asyncio.run(test_ws())
#         except Exception as e:
#             print(e)