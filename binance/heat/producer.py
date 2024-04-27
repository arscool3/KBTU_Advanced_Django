import asyncio
import json
from confluent_kafka import Producer
import websockets

producer = Producer({'bootstrap.servers': 'localhost:9092'})
topic = 'main_topic'



async def produce_data():
    try:
        async with websockets.connect("ws://localhost:8081/data") as websocket:
            while True:
                data = await websocket.recv()
                producer.produce(topic, value=json.dumps(data))
                producer.flush()
                print("done")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    asyncio.run(produce_data())
