import asyncio
import json
import time

import confluent_kafka
import websockets

producer = confluent_kafka.Producer(
    {"bootstrap.servers": "localhost:9092"},
)

topic = "binance_topic"


async def produce():
    try:
        async with websockets.connect("ws://localhost:8081/binance") as websocket:
            while True:
                data = await websocket.recv()
                producer.produce(topic=topic, value=json.dumps(data))
                producer.flush()
                print(f"Sent message: {data}")
                time.sleep(1)
    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    asyncio.run(produce())