import json
import time
import uuid

import confluent_kafka

producer = confluent_kafka.Producer(
    {"bootstrap.servers": "localhost:9092"}
)

topic = "message_topic"


def produce_message(message):
    producer.produce(topic=topic, value=json.dumps(message).encode('utf-8'))
    producer.flush()
    print("Message sent to consumer")


def produce(message):
    while True:
        produce_message(message)
        time.sleep(1)

