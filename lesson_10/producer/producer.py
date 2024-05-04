import os
import pickle
import time

import confluent_kafka
import httpx

import sys

import asyncio
import websockets
import json

print("\n\n\n\n\nSTART\n\n\n\n")

KAFKA_BOOTSTRAP = os.environ.get("KAFKA_BOOTSTRAP", "localhost: 9092")

producer = confluent_kafka.Producer({"bootstrap.servers": KAFKA_BOOTSTRAP})

binance_host = os.environ.get("INTERNAL_BINACE_HOST", "localhost:8543")
topic = os.environ.get("DEFAULT_TOPIC", "main_topic")

print("\n\n\n\n\nCONNECTED\n\n\n\n")


def request_to_binance():
    time.sleep(1)  # to not DOS a server
    url = f"http://{binance_host}/fake/binance/data/"
    print(url)
    response = httpx.get(url)
    return response.json()


def produce(res: dict) -> None:
    to_send = pickle.dumps(res)
    producer.produce(topic=topic, value=to_send)
    producer.flush()


async def produce_ws(res: dict) -> None:
    to_send = pickle.dumps(res)
    producer.produce(topic=topic, value=to_send)
    producer.flush()


async def ws():
    try:
        async with websockets.connect(f"ws://{binance_host}/ws/fake/binance/data/") as websocket:
            print("Connected")
            while True:
                print("Receiving data")
                data = await websocket.recv()
                print(data)
                await produce_ws(json.loads(data))
    except websockets.exceptions.ConnectionClosedOK:
        print("Connection closed")

if __name__ == "__main__":
    if sys.argv[1] == "ws":
        asyncio.run(ws())
    else:
        while True:
            res = request_to_binance()
            produce(res)
