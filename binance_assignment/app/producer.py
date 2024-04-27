import asyncio
import time

import confluent_kafka
import websockets

from schemas import BinanceDeal

producer = confluent_kafka.Producer(
    {"bootstrap.servers": "localhost:9092"}
)

topic = "main_topic"


async def produce_message():
    url = 'ws://127.0.0.1:8000/data'
    try:
        async with websockets.connect(url) as websocket:
            while True:
                data = await websocket.recv()
                producer.produce(topic, data)
    except websockets.exceptions.ConnectionClosedOK as e:
        print('Connection closed')


asyncio.run(produce_message())


