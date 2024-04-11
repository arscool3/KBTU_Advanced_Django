import json
import time

import confluent_kafka
import requests

from config import BINANCE_URL

producer = confluent_kafka.Producer(
    {"bootstrap.servers": "localhost:9092"},
)

topic = "binance_topic"


def produce():
    try:
        while True:
            data = requests.get(BINANCE_URL).json()
            producer.produce(topic=topic, value=json.dumps(data))
            producer.flush()
            print(f"Sent message: {data}")
            time.sleep(1)
    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    produce()
