import os
import time

import confluent_kafka
import httpx

from consumer.consumer import consume_message, consumer_data

TOPIC = os.environ.get("DEFAULT_TOPIC", "main_topic")

# import asyncio

url = "http://localhost:8001/health-check/"

consumer = confluent_kafka.Consumer(
    consumer_data
)
consumer.subscribe([TOPIC])


def process():
    while True:
        try:
            time.sleep(0.1)
            response = httpx.get(url)

            response.raise_for_status()
            print("fdafdsfasfds")
        except:
            consume_message(consumer)
